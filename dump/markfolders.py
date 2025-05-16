import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

def rename_files_from_subfolders():
    # Create the main window
    root = tk.Tk()
    root.title("Subfolder File Renamer")
    root.geometry("600x400")
    
    # Variable to store selected folder path
    selected_folder = filedialog.askdirectory(
        title="Select parent folder",
    )
    # Function to process files in subfolders
    subfolders = [f for f in os.listdir(selected_folder) if os.path.isdir(os.path.join(selected_folder, f))]
            
            # Process each subfolder
    for subfolder in subfolders:
        subfolder_path = os.path.join(selected_folder, subfolder)
        for root_dir, dirs, files in os.walk(subfolder_path):
            for file in files:
                apply_png_overlay(video_path, cage_number,width,autocount=None)
    root.destroy()

def apply_png_overlay(video_path, cage_number,width,autocount=None):
    """
    Apply a transparent PNG overlay to a video using FFmpeg.
    
    Args:
        video_path (str): Path to the input video.
        cage_number (str): Path to the transparent PNG overlay.
    
    Returns:
        str: Path to the output video file.
    """
    # Get the directory and filename of the input video
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join("C:/Users/Labo Samaha/Desktop/.LabGym/2) MARKED videos", f"{video_name}_marked.mp4")
    
    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,
            "-i", f"C:/Users/Labo Samaha/Desktop/.LabGym/z_misc_DONOTTOUCH/cage{cage_number}_{width}.png ",
            "-filter_complex", "[0][1]overlay=x=0:y=0",
            "-c:v", "h264_nvenc",
            "-y",  # Overwrite output file if it exists
            "-an",
            output_path
        ]
        
        print("Starting overlay process...")
        subprocess.run(cmd, check=True)
        print(f"Overlay completed successfully! Output saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during overlay process: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None
    
if __name__ == "__main__":
    rename_files_from_subfolders()
