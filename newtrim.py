from pathlib import Path
from common.common import select_video,format_time_colons,remove_other,makefolder,clear_gpu_memory,error,askstring,custom_dialog,group_from_end,findval,assignval,askint
from addtopss import addtopss
import subprocess
import os, sys


def batch_trim(input_path: str, start_times: list[str], end_times: list[str],  output_folder: str,count:int = 1,) -> bool:
    """Trims a video into multiple clips in a single FFmpeg process for efficiency.

    This function constructs and executes a single FFmpeg command to extract
    multiple segments from a video file. This is significantly faster than
    calling FFmpeg repeatedly in a loop, as the input video is only read
    and decoded once. It leverages NVIDIA's CUDA for hardware acceleration.

    Args:
        input_path (str): Path to the input video file.
        start_times (list[str]): A list of start timestamps for the clips,
            formatted as "HH:MM:SS".
        end_times (list[str]): A list of end timestamps for the clips,
            formatted as "HH:MM:SS". Must be the same length as start_times.
        output_folder (str): The directory where the output video clips
            will be saved.
        count (int, optional): The starting number for the output file naming
            sequence (e.g., `basename_001.mp4`). Defaults to 1.

    Returns:
        bool: True if the FFmpeg command executes successfully. Raises a
              `subprocess.CalledProcessError` on failure.
    """

    base_name = os.path.splitext(os.path.basename(input_path))[0]

    cmd = [
        "ffmpeg",
        "-hwaccel", "cuda",
        "-hwaccel_output_format", "cuda", 
        "-c:v", "h264_cuvid",
        "-i", input_path,
    ]
    for i, starttime in enumerate(start_times):
        output_title = f"{base_name}_{count:03d}.mp4"
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
    print(cmd)
    subprocess.run(cmd, check=True)
    return output_path
    
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
        map(format_time_colons,start_times) # format as HH:MM:SS
    )

    batch_size:int = askint(msg="How many clips at once?",title="Batch size",fill=findval("batch_size"))
    assignval("batch_size",batch_size)
    
    start_times_list = group_from_end(start_times, batch_size)
    print(f"{start_times_list=}",)


    end_times = list(
        map(format_time_colons,end_times) # format as HH:MM:SS
    )
    end_times_list = group_from_end(end_times, batch_size)
    print(f"{end_times_list=}")


    if len(start_times) > 1 and len(file_paths) == 1 or len(file_paths) > 1:  # folder needed if multiple trims for one file
        output_folder = makefolder(file_paths[0],foldername="trimmed-")
    else: # same folder if only one single trim output
        output_folder = os.path.dirname(file_paths[0])
    all_processing_complete = False
    complete = None
    
    if len(end_times) == len(start_times): # making sure no timestamps are missing in start/end inputs
        for vid in file_paths:
            new_count = 1
            for count, start_list in enumerate(start_times_list):
                complete = batch_trim(vid,start_list,end_times_list[count],output_folder,count=new_count)
                new_count += len(start_list)
            if complete:
                clear_gpu_memory()
            else:
                error(f"Error with video: {os.path.basename(vid)}\n\nStart times = {' '.join(start_times)}\nEnd times = {' '.join(start_times)}\n\noutput:{output_folder}")
                return
        all_processing_complete = clear_gpu_memory() # -> True
    else:
        error(f"Must enter same # of start times as end times.\{start_times=}\nEnd times = {end_times=}")
    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and output_folder:
        os.startfile(output_folder)

if __name__ == "__main__":
    main()
