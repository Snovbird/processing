from pathlib import Path
from common.common import *
from addtopss import addtopss
import subprocess
import os, sys

def batch_trim(input_path: str, start_times: list[str], end_times: list[str],  output_folder: str,count:int = 1,skip_overflow=True) -> bool:
    """
    Trims a video into multiple clips for given **seconds** timestamps

    Args:
        input_path (str): Path to the input video file.
        start_times (list[str]): A list of start timestamps for the clips, formatted as "HH:MM:SS".
        end_times (list[str]): A list of end timestamps for the , formatted as "HH:MM:SS". Must be the same length as start_times.
        output_folder (str): The directory where the output video clips will be saved.
        count (int, optional): The starting number for the output file naming sequence (e.g., `basename_001.mp4`). Defaults to 1. Necessary since a same video might need to be batch trimmed twice due to the batch limit of 7 (memory limitation of GPU)
        skip_overflow (bool, optional): if True (default), will compare start_times to video length. If start time > total len --> timestamp will be skipped 
    Returns:
        bool: True if the FFmpeg command executes successfully. Raises a `subprocess.CalledProcessError` on failure.
    """
    if skip_overflow:
        vidlen = get_duration(input_path)[1]
        ok = []
        for time in start_times:
            time = time.replace(":", "").zfill(6)
            secs = int(time[0:2]) * 3600 + int(time[2:4]) * 60 + int(time[4:6])
            if secs < vidlen:
                ok.append(format_time_colons(time)) # format needed by ffmpeg = HH:MM:SS not HHMMSS
        start_times = ok
        if len(start_times) != len(end_times):
            end_times = end_times[:len(start_times)]
        if not start_times:
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
        output_title = f"{base_name}-{count:03d}.mp4"
        output_path = os.path.join(output_folder, output_title)
        
        cmd.extend([
            "-ss", starttime,
            "-to", end_times[i],
            "-c:v", "h264_nvenc",
            "-preset", "p1",
            "-gpu", "0",  # Specify GPU index
            "-an",
            "-y",
            output_path
        ])
        count += 1

    if start_times:
        print(cmd)
        subprocess.run(cmd, check=True)
        return output_path
    
def process_from_start(file_paths:list[str],start_times:list[str],end_times:list[str],trims_foldername = "Trims",batch_size:int = None):
    """
    Groups start timestamps in SECONDS for a given batch_size value. Group size = amount of trimmed outputs per batch. Creates output folder in the input video dir IF NEEDED. Calls batch_trim to initiate trimming 
    Args:
        file_paths (list[str]): list of video paths to be batch trimmed
        start_times (list[str]): list of trim start timestamps in **seconds**
        end_times (list[str]): list of trim end timestamps in **seconds**. Must be the same length as start_times
        trims_foldername (str, optional): Name of the created trim ouputs folder. Default name = "Trims". 
        batch_size (int): number of outputs per batch. Adjust this value depending on GPU memory capabilities. Prompts if not provided




    """
    start_times = list(
        map(format_time_colons,start_times) # format as HH:MM:SS
    )
    if not batch_size:
        batch_size:int = askint(msg="How many trimmed video outputs at once?",title="Batch size",fill=findval("batch_size"))
        assignval("batch_size",batch_size)
    
    # Group timestamps in descending order to avoid GPU memory overload
    start_times_list = group_from_end(start_times, batch_size)
    print(f"{start_times_list=}",)
    end_times = list(
        map(format_time_colons,end_times) # format as HH:MM:SS
    )
    end_times_list = group_from_end(end_times, batch_size)
    print(f"{end_times_list=}")

    if (len(start_times) > 1 and len(file_paths) == 1) or len(file_paths) > 1:  # folder needed if multiple trims for one file
        output_folder = makefolder(file_paths[0],foldername=trims_foldername,
                                   start_at_1=False if trims_foldername != "Trims" else True)
    else: # same folder if only one single trim output
        output_folder = os.path.dirname(file_paths[0])
    all_processing_complete = False
    complete = None
    
    if len(end_times) == len(start_times): # making sure no timestamps are missing in start/end inputs
        for vid in file_paths:
            new_count = 1
            for count, start_list in enumerate(start_times_list):
                try:
                    complete = batch_trim(vid,start_list,end_times_list[count],output_folder,count=new_count)
                except subprocess.CalledProcessError as e:
                    assignval("TRIM_ERROR",f"FFmpeg error with video: {os.path.basename(vid)}\n\nStart times = {' '.join(start_times)}\nEnd times = {' '.join(end_times)}\n\noutput:{output_folder}\n\nError details: {e}")
                    error(f"FFmpeg error with video: {os.path.basename(vid)}\n\nStart times = {' '.join(start_times)}\nEnd times = {' '.join(end_times)}\n\noutput:{output_folder}\n\nError details: {e}")
                    break
                new_count += len(start_list)
            if complete:
                clear_gpu_memory()
            else:
                error(f"Error with video: {os.path.basename(vid)}\n\nStart times = {' '.join(start_times)}\nEnd times = {' '.join(start_times)}\n\noutput:{output_folder}")
                return
        all_processing_complete = clear_gpu_memory() # -> True
    else:
        error(f"Must enter same # of start times as end times.\n{start_times=}\nEnd times = {end_times=}")
    return output_folder,all_processing_complete

def trim_DS_auto(file_paths:list[str],first:str=None,which=["DS+", "DS-"],start_time=20,interval_duration=55,batch_size = 7,):
    """
    Automatically find DS+ and DS- timestamps for given videos
    Args:
        video (str): path to video
        first (str): Options = `DS+` or `DS-`. The first cue occuring in the experiment video.
        which (str, optional): options = `DS+`, `DS-`,`ALL IN ONE` or `BOTH SEPARATE`. Default will creeate both DS+ and DS- folder
        start_time (int): Time in seconds when the first trial (illuminated light) occurs.
        interval_duration (int): Length of trimmed outputs. Increase to make sure to account for shifts in trial timestamps (will include ITI where no cue light is illuminated).
        batch_size (int, optional): number of outputs at once for a SINGLE video
    """
    okay = [which] if isinstance(which,str) else which
    from trial_formula import trial_formula
    from addtopss import addtopss
    if not first: # automatically use the name to determine if it is DS+ or DS-
        first = os.path.basename(os.path.dirname(file_paths[0])).split(" ")[-1]
    
    if first == "DS+":
        if "DS+" in okay:
            DS_plus_plusfirst_start:str = trial_formula(plus_or_minus_first="DS+",extract_which="DS+",start_time=start_time)
            DS_plus_plusfirst_end:list[str] = addtopss(DS_plus_plusfirst_start, toadd=interval_duration, HHMMSS_or_frames="HHMMSS")
            process_from_start(file_paths,DS_plus_plusfirst_start.split("."),DS_plus_plusfirst_end,trims_foldername="DS+",batch_size=batch_size)
        if "DS-" in okay:
            DS_minus_plusfirst_start:str = trial_formula(plus_or_minus_first="DS+",extract_which="DS-",start_time=start_time)
            DS_minus_plusfirst_end:list[str] = addtopss(DS_minus_plusfirst_start, toadd=interval_duration, HHMMSS_or_frames="HHMMSS")
            process_from_start(file_paths,DS_minus_plusfirst_start.split("."),DS_minus_plusfirst_end,trims_foldername="DS-",batch_size=batch_size)
    elif first == "DS-":
        if "DS+" in okay:
            DS_plus_minusfirst_start:str = trial_formula(plus_or_minus_first="DS+",extract_which="DS-",start_time=start_time)
            DS_plus_minusfirst_end:list[str] = addtopss(DS_plus_minusfirst_start, toadd=interval_duration, HHMMSS_or_frames="HHMMSS")
            process_from_start(file_paths,DS_plus_minusfirst_start.split("."),DS_plus_minusfirst_end,trims_foldername="DS+",batch_size=batch_size)
        if "DS-" in okay:
            DS_minus_minusfirst_start:str = trial_formula(plus_or_minus_first="DS-",extract_which="DS-",start_time=start_time)
            DS_minus_minusfirst_end:list[str] = addtopss(DS_minus_minusfirst_start, toadd=interval_duration, HHMMSS_or_frames="HHMMSS")
            process_from_start(file_paths,DS_minus_minusfirst_start.split("."),DS_minus_minusfirst_end,trims_foldername="DS-",batch_size=batch_size)
    else:
        error(f"{first} is not implemented yet")
        return

def main():
    try:
        # Get argument
        startpath:str = sys.argv[1]
        
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
        startpath:str = ''
    
    # COLLAPSE FOR VISIBILITY
    if True:
        file_paths = select_video(title=f"Select Video(S) to TRIM",path=startpath)
        if not file_paths:
            print("No file selected. Exiting...")
            return
        start_times = askstring("Start time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):","Input Start Times")
        if start_times is None:
            print("Exiting... since start_times is None")
            return
        start_times = remove_other(start_times).split(".")

        handling_end_times = custom_dialog(msg="Enter automatically a given number of seconds or FULL end times string?",title="Ending times",op1="Automatic",op2="FULL STRING")
        if handling_end_times is None:
            print("Exiting... since handling_end_times is None")
            return

        if handling_end_times == "Automatic":
            end_times = addtopss(start_times,HHMMSS_or_frames="HHMMSS")
            print(end_times)
        elif handling_end_times == "FULL STRING":
            end_times = askstring("Input Values", "End time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::")
            if end_times is None:
                print("Exiting since end_times is None")
                return
            end_times = remove_other(end_times).split(".")
        if end_times is None:
            print("Exiting since end_times is None")
            return

    output_folder,all_processing_complete = process_from_start(file_paths,start_times,end_times)    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and output_folder:
        os.startfile(output_folder)

if __name__ == "__main__":
    trim_DS_auto(file_paths=select_video(),first="DS+")