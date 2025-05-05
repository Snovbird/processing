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

def main():
    root = tk.Tk()
    root.withdraw()
    try:
        file_paths = filedialog.askopenfilenames(title="Select a Video File", 
                                            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
                                            initialdir="C:/Users/Labo Samaha/Desktop/LabGym/")
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
    
    start_time = format_time_input(start_time)
    
    end_time = simpledialog.askstring(title, "NO COLONS. END time (HHMMSS):")
    if end_time is None:
        print("End time not provided. Exiting...")
        return
    
    end_time = format_time_input(end_time)
    
    root.destroy()
    print("Start time:", start_time)
    print("End time:", end_time)
    for video in file_paths:
        print("Selected file:", video)
        output_path = convert_to_mp4(video, start_time, end_time)
        
    if output_path:
        os.startfile(os.path.dirname(output_path))

def convert_to_mp4(input_path, start_time, end_time):
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

def open_folder(file_path):
    """
    Open the folder containing the specified file.
    
    Args:
        file_path (str): Path to the file whose folder should be opened.
    """
    folder_path = os.path.dirname(file_path)
    if platform.system() == "Windows":
        os.startfile(folder_path)  # Open folder on Windows
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", folder_path])
    else:  # Assume Linux
        subprocess.run(["xdg-open", folder_path])

if __name__ == "__main__":
    main()
