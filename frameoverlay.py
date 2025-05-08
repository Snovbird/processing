import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
import platform

def overlay_FRAMES(input_path):
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
    output_path = os.path.join(file_dir, f"{file_name}_FRAME_overlaid.mp4")
    
    try:
        # FFmpeg command to resize the video proportionally using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-i", input_path,  # Input file
            "-vf", "drawtext=fontfile=Arial.ttf:text=%{n}:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:box=1:boxcolor=0x00000000",  # overlay
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            # "-c:a", "copy",  # Copy audio without re-encoding
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
        initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/"
    )
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    # Resize the video
    for i, path in enumerate(file_paths):
        if i > 0:
            # Clear GPU memory between files
            clear_gpu_memory()
        output_path = overlay_FRAMES(path)
    
    # Open the folder containing the resized video
    if output_path:
        os.startfile(os.path.dirname(output_path))
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
    
if __name__ == "__main__":
    main()
