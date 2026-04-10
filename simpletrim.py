from common.common import *
from TRIM import trim_frames
import pyperclip, shutil,os 
from frameoverlay import overlay_FRAMES

def main():
    # Get the file path from the clipboard
    file_path = pyperclip.paste().strip('"')  
    if not os.path.isfile(file_path):
        print("not a file")
        return

    initial_dir = os.path.dirname(file_path)

    cues_corresponding = {
        "DS+": "FR",
        "DS-": "BL",
        "CS+": "BR"
    }

    for cue, light in cues_corresponding.items():
        if cue in os.path.dirname(file_path) or light in os.path.dirname(file_path):
            light = light
            break
    else:
        cue = simple_dropdown([cue for cue in cues_corresponding.keys()], title="Select the cue type")
        if not cue:
            return
        light = cues_corresponding.get(cue)
    
    working_directory = find_folder_path("5-clips")
    cue_folder = os.path.join(working_directory, cue)

    foldernames = [name for name in list_folders(cue_folder) if "." not in name]
    folderpaths = [path for path in list_folderspaths(cue_folder) if "." not in os.path.basename(path)]
    behavior_name_path = {name.replace(light,"").replace(cues_corresponding.get(cue),""): 
                          path for name,path in zip(foldernames,folderpaths)}

    overlaid = overlay_FRAMES(file_path, working_directory,center=True)
    os.startfile(overlaid)
    fill = "" # save input if len(starts) != len(ends) to ask question again

    toprocess = []
    snippet_number = 1
    while True:
        times = askstring("Enter the trim times (start.end) in seconds, separated by periods.",title=f"{os.path.basename(file_path)}",fill=fill)
        if not times and len(toprocess) ==0:
            return
        elif not times and len(toprocess) !=0:
            break
        times=times.split(".")
        starts = [i for n, i in enumerate(times) if n % 2 == 0]
        ends = [i for n,i in enumerate(times) if n % 2 != 0]
        if len(starts) != len(ends):
            print("Please enter same number of start and end times.")
            continue

        for start, end in zip(starts, ends):
            if (int(end) - int(start) + 1) % 3 == 0:
                action = custom_dialog(msg=f"add 1 frame or remove 2?",title=f"{start}-{end}",op1="+1",op2="-2")
                if not action:
                    return
                if action == "+1":
                    end = str(int(end)+1)
                elif action == "-2":
                    end = str(int(end)-2)
            elif (int(end) - int(start) - 1) % 3 == 0:
                action = custom_dialog(msg="add 2 frames or remove 1?",title=f"{start}-{end}",op1="+2",op2="-1")
                if not action:
                    return
                if action == "+2":
                    end = str(int(end)+2)
                elif action == "-1":
                    end = str(int(end)-1)

            options = list(behavior_name_path.keys())
            behavior = simple_dropdown(options, msg=f"Select behavior for snippet#{snippet_number}: {start}-{end}",title=f"#{snippet_number}: {start}-{end}") 
            if not behavior and len(toprocess) ==0:
                return
            elif not behavior and len(toprocess) !=0:
                break
            snippet_number += 1
            behavior_folder = behavior_name_path.get(behavior)
            toprocess.append({(start, end): behavior_folder})

    
    for time_and_folder in toprocess:
        time, behavior_folder = time_and_folder.items()
        start, end = time
        trim_frames(input_path=file_path, output_folder=behavior_folder, start_time=start, end_time=end, show_terminal=False,all_name_with_timestamps=True)

    for folderpath in list_folderspaths(initial_dir):
        if "original" in os.path.basename(folderpath):
            originals_folder = folderpath
            break
    else:
        originals_folder = makefolder(initial_dir, "originals",start_at_1=False)
    shutil.move(file_path, os.path.join(originals_folder, os.path.basename(file_path)))
    os.remove(overlaid)
if __name__ == "__main__":
    main()