#! py -3.10
from common.common import *
import wx,os
# Queue-able processes
from concatenate import concatenate
from extractpng import extractpng
from frameoverlay import overlay_FRAMES
from markersquick import apply_png_overlay
from newtrim import trim_DS_auto
import sys


functions = [trim_DS_auto,apply_png_overlay,concatenate,extractpng,overlay_FRAMES]

from LabGym.analyzebehavior import AnalyzeAnimal
def generate_examples(video_path, output_folder, length=3):
    """
    Uses LabGym's AnalyzeAnimal class to generate examples of minimal length.
    """
    
    # 1. Initialize the class
    aa = AnalyzeAnimal()
    
    # 2. Prepare the parameters. We set length=3 as the minimum frame requirement.
    # Note: animal_number determines how many objects are tracked
    aa.prepare_analysis(
        path_to_video=video_path,
        results_path=output_folder,
        animal_number=1, # Change if you have more than 1 animal
        length=length,   # Minimum 3 frames
        categorize_behavior=False, # We just want generation, not classification
        animation_analyzer=False,
    )
    
    # 3. Generate the data
    # skip_redundant=1 means it will generate an example clip for every frame step
    # background_free=True isolates the animal, making the background black
    aa.generate_data(background_free=True, black_background=True, skip_redundant=1)
    
    print(f"Finished generating {length}-frame examples in {output_folder}")


def queue():
    functions_str:list[str] = [str(func).split(" ")[1] for func in functions] 
    ind = simple_dropdown(functions_str,return_index=True)
    if ind is None:
        return
    sel = functions[ind]
    sel_name = functions_str[ind]

    videos = []
    if custom_dialog("Use last input videos?","Input",op1="Yes",op2="No") == "Yes":
        videos = findval("last_input_videos")
    else:
        folder_or_file_explorer = custom_dialog("Select files or folders?","Input Handling",op1="Files",op2="Folders")
        selection = True
        
        if folder_or_file_explorer == "Folders":
            while selection:
                selection = select_folder(f"Select folder. Cancel to stop file explorer loop",path=os.path.dirname(selection) if isinstance(selection,str) else False)
                if selection:
                    print(f"{selection=}")
                    videos.append([os.path.join(selection,filename) for filename in list_files_ext(selection,ext=".mp4")])
            
        elif folder_or_file_explorer == "Files":
            while selection:
                selection = select_video(f"Select videos. Cancel to stop file explorer loop")
                if selection:
                    videos.append(selection)
        assignval("last_input_videos",videos)
    count = 0
    
    if sel_name == "trim_DS_auto":
        first_cue = custom_dialog("What is the first cue for experiments?","Trim setting",op1="DS+",op2="DS-")
        which = simple_dropdown(["DS+","DS-","ALL IN ONE","BOTH SEPARATE"])
        starttime = askint("Start time in seconds?","Trim setting",fill=0)
        for group in videos:
            trim_DS_auto(group,which=which,first=first_cue,start_time=starttime) # DS+ first specified for predictable light order. Change for DS+/DS- first unpredictable
            count += len(group)
    else:
        for group in videos:
            output_folder = makefolder(group[0],"Processed videos-")
            for vid in group:  
                sel(vid, output_folder=output_folder)
                count +=1
    return count,sel_name

def main ():
    pythonver = os.path.dirname(sys.executable)
    if pythonver != "Python310":
        error(f"Please run python310 instead of {pythonver}")

if __name__ == "__main__":
    c,sel_name = queue()
    msgbox(f"Successfully used {sel_name} on {c} videos")