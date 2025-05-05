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

def main():
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(title="Select a Video File", 
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if not file_path:
        print("No file selected. Exiting...")
        return
    
    title = "Input Values"
    
    start_times = simpledialog.askstring(title, "Start times separated by comma (HHMMSS,HHMMSS...):").split(",")
    if start_times is None:
        print("Start time not provided. Exiting...")
        return
    for i in range(len(start_times)):
        start_times[i] = format_time_input(start_times[i])

    end_times = simpledialog.askstring(title, "End times separated by comma (HHMMSS,HHMMSS...):").split(",")
    if end_times is None:
        print("End time not provided. Exiting...")
        return
    for i in range(len(end_times)):
        end_times[i] = format_time_input(end_times[i])

    print("Selected file:", file_path)
    print("Start time:", start_times)
    print("End time:", end_times)
    root.destroy()

    if len(end_times) == len(start_times):
        for count in range(len(start_times)):
            output_path = convert_to_mp4(file_path, start_times[count], end_times[count],count)
    else:
        messagebox.showerror("ERROR", "Must enter same # of start times as end times")
    if output_path:
        os.startfile(os.path.dirname(output_path))

def convert_to_mp4(input_path, start_times, end_time,count):
    """
    Convert a media file to MP4 format using FFmpeg
    
    Args:
        input_path (str): Path to the input file
        start_times (str): Start time for trimming (HH:MM:SS)
        end_time (str): End time for trimming (HH:MM:SS)
    
    Returns:
        str: Path to the output MP4 file
    """
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    
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

if __name__ == "__main__":
    main()
