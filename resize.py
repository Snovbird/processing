import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
from common.common import clear_gpu_memory

def resize_video_with_ffmpeg(input_path, width):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    
    Args:
        input_path (str): Path to the input video file.
        width (int): Desired width for the resized video.
    
    Returns:
        str: Path to the resized video file.
    """
    # Get the directory and filename of the input video
    file_dir = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(file_dir, f"{file_name}-RESIZED{width}.mp4")
    
    try:
        # FFmpeg command to resize the video proportionally using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-hwaccel_output_format", "cuda",  # Keep frames in GPU memory
            "-i", input_path,  # Input file
            "-vf", f"scale_cuda={width}:-2",  # Resize with proportional height
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            "-y",  # Overwrite output file if it exists
            "-an",
            output_path
        ]
        
        print("Starting video resizing...")
        subprocess.run(cmd, check=True)
        print(f"Resizing completed successfully! Resized video saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during resizing: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select a video file
    file_paths = filedialog.askopenfilenames(
        title="Select one Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
        initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/0) RECORDINGS"
    )
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    # Ask the user for the desired width
    width = simpledialog.askinteger("Input Width", "Enter the desired width (e.g., 1280):")
    if not width:
        print("No width provided. Exiting...")
        return
    elif width % 32 != 0:
        messagebox.showerror("ERROR", "Width MUST be a multiple of 32\nExamples: 1920, 1280, 1024, 480")
        return
    for i, path in enumerate(file_paths):
        if i > 0:
            # Clear GPU memory between files
            pass
        output_path = resize_video_with_ffmpeg(path,width)
    clear_gpu_memory()
    # Open the folder containing the resized video
    if output_path:
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()
