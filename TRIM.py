import os
import subprocess
from common.common import clear_gpu_memory,custom_dialog,select_video,askstring,makefolder,error,format_time_colons,remove_other
import sys
from addtopss import addtopss



def trim_frames(input_path: str, start_time:str, end_time:str,count,output_times=False,foldername=None):
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    if output_times == True:
        output_name = f"{file_name}-trim({start_time}-{end_time}).mp4"
    else:
        output_name = f"{file_name}.mp4"
    
    if foldername:
        output_path = os.path.join(foldername, output_name)
    else:
        file_dir = os.path.dirname(input_path)
        output_path = os.path.join(file_dir, output_name)

    try:
        cmd = [

            "ffmpeg", 
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-c:v", "h264_cuvid",
            "-i", input_path, 
            "-vf", f'trim=start_frame={start_time}:end_frame={end_time},setpts=PTS-STARTPTS', 
            "-c:v", "h264_nvenc",  
            "-preset", "p1",
            "-af", f'aresample=async=1',        
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not on PATH.")
        return None

def trim_timestamps(input_path, start_time, end_time, count=1, output_times=False,foldername=None):
    print(f"trim_video_timestamps_accelerated(input_path={input_path}, start_time={start_time}, end_time={end_time}, count=1=, output_times={output_times},foldername={foldername})")
    startforname = start_time.replace(":", "")
    endforname = end_time.replace(":", "")
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    if output_times == True:
        output_name = f"{file_name}-trim({startforname}-{endforname}).mp4"
    else:
        output_name = f"{file_name}.mp4"
        
    # Create unique output path for each segment
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, output_name)
        while os.path.exists(output_path):
            count +=1
            output_name = f"{file_name}{count}.mp4"
            output_path = os.path.join(foldername, output_name)

    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, output_name)
    
    try:
        # GPU-accelerated command for a single segment
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-c:v", "h264_cuvid",
            "-i", input_path,
            "-ss", start_time,
            "-to", end_time,
            "-c:v", "h264_nvenc",
            "-preset", "p1",
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd))
        # print(f"START:{start_time:*>40}]\nEND:{end_time:*>40}")
        subprocess.run(cmd, check=True)    
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    
def main():
    startpath = ''
    # Check if a command-line argument was provided (e.g., from the AHK script)
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        # Check if the argument is a valid directory path
        if os.path.isdir(path_arg):
            startpath = path_arg
        else:
            # If not a full path, try to construct one from common locations
            possible_paths = [
                os.path.join(os.path.expanduser("~"), path_arg),      # User folder
                os.path.join(os.path.expanduser("~"), "Desktop", path_arg), # Desktop
                os.path.join("C:\\", path_arg)                       # Root drive
            ]
            for path in possible_paths:
                if os.path.isdir(path):
                    startpath = path
                    break
    
    file_paths = select_video(title=f"Select Video(S) to TRIM",path=startpath)
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    start_times = remove_other(askstring("Start time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):","Input Start Times")).split(".")
    if start_times is None:
        print("Exiting... since start_times is None")
        return

    handling_end = custom_dialog(msg="Enter automatically a given number of seconds or FULL end times string?",title="Ending times",op1="Automatic",op2="FULL STRING")
    if handling_end is None:
        print("Exiting... since handling_end is None")
        return
    
    unitoption = custom_dialog(msg="HHMSS or Frames?",title="Unit used",op1="HHMMSS",op2="Frames")
    if unitoption is None:
        print("Exiting... since unitoption is None")
        return

    if handling_end == "Automatic":
        end_times = addtopss(start_times,HHMMSS_or_frames=unitoption)
        print(end_times)
    elif handling_end == "FULL STRING":
        end_times = remove_other(askstring("Input Values", "End time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::")).split(".")
    
    if end_times is None:
        print("Exiting since end_times is None")
        return
    
    
    if len(start_times) == 1: 
        # output_answer = custom_dialog("File name","Include timestamps in file name?", op1="Yes", op2="no") 
        output_answer = True
        if output_answer == 'Yes':
            output_answer = True
    else:
        output_answer = False

    if len(start_times) > 1 and len(file_paths) == 1 or len(file_paths) > 1:  # folder needed if multiple trims for one file
        foldername = makefolder(file_paths[0],foldername="trimmed-")
    # elif len(file_paths) > 1:
    #     foldername = makefolder(file_paths[0],foldername="trimmed-")
    else:
        foldername = None
    all_processing_complete = False
    output_path = None
    if len(end_times) == len(start_times):
        for count, start_time in enumerate(start_times):
            end_time = end_times[count]
            if unitoption == 'HHMMSS':
                start_time = format_time_colons(start_time)
                end_time = format_time_colons(end_time)
                print("Start time:", start_time)
                print("End time:", end_time)
                for path in file_paths:
                    output_path = trim_timestamps(path, start_time, end_time, count,output_times=output_answer, foldername=foldername)    
            elif unitoption == 'Frames':
                for path in file_paths:
                    output_path = trim_frames(path, start_time, end_time, count, output_times=output_answer,foldername=foldername)
                
        all_processing_complete = clear_gpu_memory() # -> True
    else:
        print("ERROR", f"Must enter same # of start times as end times.\nStart times = {start_times}\nEnd times = {end_times}")
    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and len(file_paths) > 1 and foldername and output_path:
        os.startfile(foldername)
    elif all_processing_complete and output_path:
        os.startfile(os.path.dirname(output_path))
    else:
        error("processing failed")

if __name__ == "__main__":
    main()
