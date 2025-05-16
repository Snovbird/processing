import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import subprocess
import platform

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

def trim_video_timestamps(input_path, start_time, end_time):
    """
    Convert a media file to MP4 format using FFmpeg
    
    Args:
        input_path (str): Path to the input file
        start_time (str): Start time for trimming (HH:MM:SS)
        end_time (str): End time for trimming (HH:MM:SS)
    
    Returns:
        str: Path to the output MP4 file
    """
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    
    file_dir = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(file_dir, f"{file_name}_trimmed.mp4")
    
    try:
        cmd = [
            "ffmpeg", 
            "-i", input_path, 
            "-c:v", "h264_nvenc",  
            "-ss", start_time,      
            "-to", end_time,        
            "-y",                   
            output_path
        ]
        
        print("Starting conversion...")
        subprocess.run(cmd, check=True)
        print(f"Conversion completed successfully!")
        print(f"Output saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def trim_frames(input_path, start_time, end_time):
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
    
    file_dir = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(file_dir, f"{file_name}_trimmed.mp4")
    
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
    
def main():
    root = tk.Tk()
    root.withdraw()
    try:
        file_paths = filedialog.askopenfilenames(title="Select one or multiple Video File(s) TO TRIM", 
                                            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
                                            initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/")
    except:
        file_paths = filedialog.askopenfilenames(title="Select a Video File", 
                                            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])  
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    title = "Input Values"
    
    start_time = simpledialog.askstring(title, "DONT ADD COLONS, just numbers. START time (HHMMSS):")
    if start_time is None:
        print("Start time not provided. Exiting...")
        return

    end_time = simpledialog.askstring(title, "NO COLONS. END time (HHMMSS):")
    if end_time is None:
        print("End time not provided. Exiting...")
        return
    root.destroy()
    if "f" not in start_time and "f" not in end_time:
        start_time = format_time_input(start_time)
        end_time = format_time_input(end_time)
        print("Start time:", start_time)
        print("End time:", end_time)
        for i, path in enumerate(file_paths):
            if i > 0:
                # Clear GPU memory between files
                pass
            output_path = trim_video_timestamps(path, start_time, end_time)
        clear_gpu_memory()   
        if output_path:
            os.startfile(os.path.dirname(output_path))
    elif "f" in start_time and "f" in end_time:
        for i, path in enumerate(file_paths):
            if i > 0:
                # Clear GPU memory between files
                pass
            output_path = trim_frames(path, start_time, end_time)
        clear_gpu_memory()
        
    if output_path: #openfile
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()
