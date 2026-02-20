from common.common import *
from TRIM import trim_frames
import pyperclip, shutil,os 
from frameoverlay import overlay_FRAMES

def main():
    # Get the file path from the clipboard

    file_path = pyperclip.paste().strip('"')  # Remove any surrounding quotes
    if "DS+" in os.path.dirname(file_path) or "FRCL" in os.path.dirname(file_path):
        light = "FRCL"
    elif "DS-" in os.path.dirname(file_path) or "BLCL" in os.path.dirname(file_path):
        light = "BLCL"
    approach_folder = find_folder_path(f"{light} light approach")
    orient_folder = find_folder_path(f"{light} light orient")
    interaction_folder = find_folder_path(f"{light} light interaction")

    working_directory = os.path.dirname(os.path.dirname(file_path)) # e.g. C:\Users\samahalabo\Desktop\5-clips\DS-

    if not os.path.isfile(file_path):
        return

    overlaid = overlay_FRAMES(file_path, working_directory,center=True)
    os.startfile(overlaid)
    fill = ""
    while True:
        times = askstring("Enter the trim times (start.end) in seconds, separated by periods.",fill=fill).split(".")
        fill = ".".join(times)
        if not times:
            return
        starts = [i for n, i in enumerate(times) if n % 2 == 0]
        ends = [i for n,i in enumerate(times) if n % 2 != 0]
        if len(starts) != len(ends):
            print("Please enter same number of start and end times.")
            continue

        outputs = []
        for start, end in zip(starts, ends):
            if (int(end) - int(start) + 1) % 3 == 0:
                action = custom_dialog(msg=f"add 1 frame or remove 2?",title=f"{start}-{end}",op1="+1",op2="-2")
                if not action:
                    continue
                if action == "+1":
                    end = str(int(end)+1)
                elif action == "-2":
                    end = str(int(end)-2)
            elif (int(end) - int(start) - 1) % 3 == 0:
                action = custom_dialog(msg="add 2 frames or remove 1?",title=f"{start}-{end}",op1="+2",op2="-1")
                if not action:
                    continue
                if action == "+2":
                    end = str(int(end)+2)
                elif action == "-1":
                    end = str(int(end)-1)


            outputs.append(
                trim_frames(input_path=file_path, output_folder=working_directory, start_time=start, end_time=end, show_terminal=False,all_name_with_timestamps=True)
                )
        basenames = [os.path.basename(output) for output in outputs]

        options = ["approach", "interaction", "orient"]
        answers = grid_selector(basenames, options_list=options).values()
        if not answers:
            continue
        else:
            break


    
    for output, answer in zip(outputs, answers):
        if answer == "approach":
            shutil.move(output, os.path.join(approach_folder, os.path.basename(output)))
        elif answer == "interaction":
            shutil.move(output, os.path.join(interaction_folder, os.path.basename(output)))
        elif answer == "orient":
            shutil.move(output, os.path.join(orient_folder, os.path.basename(output)))

    original_interaction_and_approach_folder = find_folder_path(f"originals ({light} approach + interaction)")

    shutil.move(file_path, os.path.join(original_interaction_and_approach_folder, os.path.basename(file_path)))
    os.remove(overlaid)
if __name__ == "__main__":
    main()