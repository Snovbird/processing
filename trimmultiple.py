import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import subprocess
from tkinter import messagebox
from common.common import clear_gpu_memory,custom_dialog

def format_time_input(time_input):
    """
    Format the time input to HH:MM:SS.
    
    Args:
        time_input (str): The input time as a string without colons.
    
    Returns:
        str: Formatted time as HH:MM:SS.
    """
    time_input = time_input.strip()
    
    if time_input.isdigit():
        time_input = time_input.zfill(6)
        return f"{time_input[:-4]}:{time_input[-4:-2]}:{time_input[-2:]}"
    else:
        return time_input  # Return the original input if it's not valid

def trim_frames(input_path, start_time, end_time,count,output_times=False,foldername=None):
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    
    if output_times == True:
        output_name = f"{file_name}-trim({start_time}-{end_time}).mp4"
    else:
        output_name = f"{file_name}.mp4"
    
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, output_name)
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
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
        print(" ".join(cmd), "\n*****************************************************************************************************")
        subprocess.run(cmd, check=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not on PATH.")
        return None

def trim_video_timestamps_accelerated(input_path, start_time, end_time, count, output_times=False,foldername=None):
    startforname = start_time.replace(":", "")
    endforname = end_time.replace(":", "")
    if output_times == True:
        output_name = f"{file_name}-trim({startforname}-{endforname}).mp4"
    else:
        output_name = f"{file_name}.mp4"
    # Create unique output path for each segment
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
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
        subprocess.run(cmd, check=True)    
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


def makefolder(file_path, count=1):
    # Get directory containing the file
    folder_path = os.path.dirname(file_path)
    
    # Get just the filename without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create folder name
    resized_folder_name = f"trimmed-{count}"
    
    # Create full path to new folder
    resized_folder_path = os.path.join(folder_path, resized_folder_name)
    
    # Check if folder exists and print debug info
    print(f"Checking if folder exists: {resized_folder_path}")
    print(f"Folder exists: {os.path.exists(resized_folder_path)}")
    
    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        # messagebox.showerror("ERROR", f"DELETE the folder {resized_folder_name}")
        # os.startfile(os.path.dirname(resized_folder_path))
        # return None
        return makefolder(file_path, count+1)
    else:
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
    return resized_folder_path
    
def remove_other(stringinput):
    a = ""
    for i in stringinput:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
            a += i
    return a

def main():
    root = tk.Tk()
    root.withdraw()
    
    file_paths = filedialog.askopenfilenames(title="Select one or multiple Video File(s)", 
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    start_times = remove_other(simpledialog.askstring("Input Values", "Start time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):")).split(".")
    
    if start_times is None:
        print("Exiting...")
        return
    # for i in range(len(start_times)):
    #     start_times[i] = format_time_input(start_times[i])

    end_times = remove_other(simpledialog.askstring("Input Values", "End time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::")).split(".")
    
    unitoption = custom_dialog("Unit","What is your format?", op1="HHMMSS", op2="Frames")
        

    if end_times is None:
        print("Exiting...")
        return
    # for i in range(len(end_times)):
    #     end_times[i] = format_time_input(end_times[i])

    root.destroy()
    if len(start_times) == 1: 
        output_answer = custom_dialog("File name","Include timestamps in file name?", op1="Yes", op2="no")

        if output_answer == 'Yes':
            output_answer = True
    else:
        output_answer = False
    if len(start_times) > 1 and len(file_paths) == 1:
        
        foldername = makefolder(file_paths[0])
    elif len(file_paths) > 1:
        foldername = makefolder(file_paths[0])
    else:
        
        foldername = None
    all_processing_complete = False
    output_path = None
    
    if len(end_times) == len(start_times):
        for count, _ in enumerate(start_times):
            start_time = start_times[count]
            end_time = end_times[count]
            if unitoption == 'HHMMSS':
                start_time = format_time_input(start_time)
                end_time = format_time_input(end_time)
                print("Start time:", start_time)
                print("End time:", end_time)
                for i, path in enumerate(file_paths):
                    output_path = trim_video_timestamps_accelerated(path, start_time, end_time, count,output_times=output_answer, foldername=foldername)    
                # Remove this line: os.startfile(os.path.dirname(output_path))
            elif unitoption == 'Frames':
                for i, path in enumerate(file_paths):
                    if i > 0:
                        # Clear GPU memory between files
                        pass
                    output_path = trim_frames(path, start_time, end_time, count, output_times=output_answer,foldername=foldername)
                
        clear_gpu_memory()
        all_processing_complete = True
    else:
        messagebox.showerror("ERROR", "Must enter same # of start times as end times")
    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and len(file_paths) > 1 and foldername and output_path:
        os.startfile(foldername)
    elif all_processing_complete and output_path:
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()
