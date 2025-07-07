from pathlib import Path
from common.common import select_video,format_time_colons,remove_other,makefolder,clear_gpu_memory,error,askstring,custom_dialog
from addtopss import addtopss
import subprocess
import os, sys

def get_unique_filename(base_path, format_template="{stem}_{counter:03d}{suffix}"): # no idea what any of this does
    """
    Advanced version with customizable counter format
    
    Args:
        base_path: Original file path
        format_template: Template for new name. Available variables:
                        {stem}, {suffix}, {counter}, {parent}
    """
    
    path = Path(base_path)
    
    if not path.exists():
        return str(path)
    
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    
    counter = 1
    while True:
        new_name = format_template.format(
            stem=stem,
            suffix=suffix,
            counter=counter,
            parent=parent
        )
        new_path = parent / new_name
        if not new_path.exists():
            return str(new_path)
        counter += 1

def batch_trim(input_path:str, start_times:list[str], end_times:list[str],output_path:str) -> bool:
    """
    Create multiple clips with automatic naming to avoid overwrites
    """
    if ":" not in start_times[0]:
        error("Improper start_times formatting")
        return
    if ":" not in end_times[0]:
        error("Improper end_times formatting")
        return
    
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    cmd = [
        "ffmpeg",
        "-hwaccel", "cuda",
        "-hwaccel_output_format", "cuda", 
        "-c:v", "h264_cuvid",
        "-i", input_path,
    ]
    
    for i, starttime in enumerate(start_times):
        # Generate unique filename for each clip
        output_path = f"{base_name}_{i+1:03d}.mp4"
        unique_output = get_unique_filename(output_path)
        
        cmd.extend([
            "-ss", starttime,
            "-to", end_times[i],
            "-c:v", "h264_nvenc",
            "-preset", "p1", 
            "-an",
            unique_output
        ])
    
    cmd.append("-y")
    subprocess.run(cmd,check=True)

    return True
    
def main():
    try:
        # Get argument
        startpath = sys.argv[1]
        
        # If the path doesn't exist as-is, try to construct a proper path
        if not os.path.isdir(startpath):
            # Try to match with common Windows folders
            possible_paths = [
                os.path.join(os.path.expanduser("~"), startpath),  # User folder
                os.path.join(os.path.expanduser("~"), "Desktop", startpath),    # Desktop
                os.path.join("C:\\", startpath)  # Root drive
            ]
            
            for path in possible_paths:
                if os.path.isdir(path):
                    startpath =  path
                    break

    except Exception as e:
        
        startpath = ''
 
    file_paths = select_video(title=f"Select Video(S) to TRIM",path=startpath)
    if not file_paths:
        print("No file selected. Exiting...")
        return
    start_times = remove_other(askstring("Start time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):","Input Start Times")).split(".")
    if start_times is None:
        print("Exiting... since start_times is None")
        return
    handling_end_times = custom_dialog(msg="Enter automatically a given number of seconds or FULL end times string?",title="Ending times",op1="Automatic",op2="FULL STRING")
    if handling_end_times is None:
        print("Exiting... since handling_end_times is None")
        return

    if handling_end_times == "Automatic":
        end_times = addtopss(start_times,HHMMSS_or_frames="HHMMSS")
        print(end_times)
    elif handling_end_times == "FULL STRING":
        end_times = remove_other(askstring("Input Values", "End time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::")).split(".")
    if end_times is None:
        print("Exiting since end_times is None")
        return
    
    start_times = list(
        map(format_time_colons,start_times)
    )
    end_times = list(
        map(format_time_colons,end_times)
    )
    if len(start_times) > 1 and len(file_paths) == 1 or len(file_paths) > 1:  # folder needed if multiple trims for one file
        output_folder = makefolder(file_paths[0],foldername="trimmed-")
    else: # same folder
        output_folder = os.path.dirname(file_paths[0])
    all_processing_complete = False
    
    if len(end_times) == len(start_times):
        for vid in file_paths:
            complete = batch_trim(vid,start_times,end_times,output_folder)
            if not complete:
                error(f"Error with video: {os.path.basename(vid)}\n\nStart times = {' '.join(start_times)}\nEnd times = {' '.join(start_times)}\n\noutput:{output_folder}")
        all_processing_complete = clear_gpu_memory() # -> True
    else:
        print("ERROR", f"Must enter same # of start times as end times.\nStart times = {start_times}\nEnd times = {end_times}")
    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and output_folder:
        os.startfile(output_folder)

if __name__ == "__main__":
    main()
