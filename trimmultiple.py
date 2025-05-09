import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import subprocess
import platform
from tkinter import messagebox

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

def clear_gpu_memory():
    try:
        # Reset GPU clocks temporarily to help clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False

def trim_frames(input_path, start_time, end_time,count,foldername=None):
    """
    Convert a media file to MP4 format using FFmpeg
    
    Args:
        input_path (str): Path to the input file
        start_time (str): Start frame for trimming 
        end_time (str): End frame for trimming 
    
    Returns:
        str: Path to the output MP4 file
    """
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, f"{file_name}_trimmed{count}.mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}_trimmed{count}.mp4")

    try:
        cmd = [

            "ffmpeg", 
            "-i", input_path, 
            "-c:v", "h264_nvenc",  
            "-vf", f'trim=start_frame={start_time.replace("f","")}:end_frame={end_time.replace("f","")},setpts=PTS-STARTPTS',      
            "-af", f'aresample=async=1',        
            "-y",
            "-an",                   
            output_path
        ]
        subprocess.run(cmd, check=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def trim_video_timestamps(input_path, start_times, end_time,count,foldername=None):
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, f"{file_name}_trimmed{count}.mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}_trimmed{count}.mp4")
    
    try:
        cmd = [
            "ffmpeg", 
            "-i", input_path, 
            "-c:v", "h264_nvenc",  
            "-ss", start_times,      
            "-to", end_time,        
            "-y",
            "-an",                   
            output_path
        ]
        

        subprocess.run(cmd, check=True)    
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def makefolder(file_path):
    # Get directory containing the file
    folder_path = os.path.dirname(file_path)
    
    # Get just the filename without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create folder name
    resized_folder_name = f"_{file_name}_trimmed"
    
    # Create full path to new folder
    resized_folder_path = os.path.join(folder_path, resized_folder_name)
    
    # Check if folder exists and print debug info
    print(f"Checking if folder exists: {resized_folder_path}")
    print(f"Folder exists: {os.path.exists(resized_folder_path)}")
    
    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        messagebox.showerror("ERROR", f"DELETE the folder {resized_folder_name}")
        os.startfile(os.path.dirname(resized_folder_path))
        return None
    else:
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
        return resized_folder_path
    
def main():
    root = tk.Tk()
    root.withdraw()
    
    file_paths = filedialog.askopenfilenames(title="Select one or multiple Video File(s)", 
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    start_times = simpledialog.askstring("Input Values", "Start time (HHMMSS): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):").split(".")
    
    if start_times is None:
        print("Start time not provided. Exiting...")
        return
    for i in range(len(start_times)):
        start_times[i] = format_time_input(start_times[i])

    end_times = simpledialog.askstring("Input Values", "End time (HHMMSS): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::").split(".")
    if end_times is None:
        print("End time not provided. Exiting...")
        return
    for i in range(len(end_times)):
        end_times[i] = format_time_input(end_times[i])

    root.destroy()
    if len(file_paths) > 1:
        foldername = makefolder(file_paths[0])
    else:
        foldername = None

    all_processing_complete = False
    output_path = None
    
    if len(end_times) == len(start_times):
        for count, _ in enumerate(start_times):
            start_time = start_times[count]
            end_time = end_times[count]
            if "f" not in start_time and "f" not in end_time:
                start_time = format_time_input(start_time)
                end_time = format_time_input(end_time)
                print("Start time:", start_time)
                print("End time:", end_time)
                for i, path in enumerate(file_paths):
                    if i > 0:
                        # # Clear GPU memory between files
                        # clear_gpu_memory()
                        pass
                    output_path = trim_video_timestamps(path, start_time, end_time, count, foldername)    
                # Remove this line: os.startfile(os.path.dirname(output_path))
            elif "f" in start_time and "f" in end_time:
                for i, path in enumerate(file_paths):
                    if i > 0:
                        # Clear GPU memory between files
                        pass
                    output_path = trim_frames(path, start_time.replace("f",''), end_time.replace("f",''), count, foldername)
                
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
