import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
import platform

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
    output_path = os.path.join(file_dir, f"{file_name}_RESIZED{width}.mp4")
    
    try:
        # FFmpeg command to resize the video proportionally using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-hwaccel_output_format", "cuda",  # Keep frames in GPU memory
            "-i", input_path,  # Input file
            "-vf", f"scale_cuda={width}:-2",  # Resize with proportional height
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            "-c:a", "copy",  # Copy audio without re-encoding
            "-y",  # Overwrite output file if it exists
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

def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select a video file
    file_path = filedialog.askopenfilename(
        title="Select one Video File",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")],
        initialdir="C:/Users/Labo Samaha/Desktop/LabGym/0) RAW videos"
    )
    if not file_path:
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
    # Resize the video
    output_path = resize_video_with_ffmpeg(file_path, width)
    
    # Open the folder containing the resized video
    if output_path:
        open_folder(output_path)

if __name__ == "__main__":
    main()
