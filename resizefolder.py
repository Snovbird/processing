import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
import platform

def resize_video_with_ffmpeg(input_list, width, folder_path):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    
    Args:
        input_list (list): List of paths to input video files.
        width (int): Desired width for the resized video.
        folder_path (str): Path to the directory containing the videos.
    
    Returns:
        str: Path to the folder containing resized videos.
    """
    # Create a new folder for resized videos
    resized_folder_name = f"resized_{width}"
    resized_folder_path = os.path.join(folder_path, resized_folder_name)
    
    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        messagebox.showerror("ERROR", f"DELETE the folder {resized_folder_name}")
        open_folder(resized_folder_path)
        return
    if not os.path.exists(resized_folder_path):
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
    
    for input_path in input_list:
        # Skip non-video files
        _, ext = os.path.splitext(input_path.lower())
        if ext not in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            continue
            
        # Get the filename of the input video
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        # Set output path in the new folder
        output_path = os.path.join(resized_folder_path, f"{file_name}.mp4")
        
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
            
            print(f"Resizing video: {input_path}")
            subprocess.run(cmd, check=True)
            print(f"Resizing completed successfully! Saved to: {output_path}")
        
        except subprocess.CalledProcessError as e:
            print(f"Error during resizing: {e}")
        except FileNotFoundError:
            print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
            return None
    
    return resized_folder_path

def open_folder(folder_path):
    """
    Open the specified folder.
    
    Args:
        folder_path (str): Path to the folder to open.
    """
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
    
    # Use askopenfilename to select a file
    file_path = filedialog.askopenfilename(
        title="SELECT VIDEO - ALL VIDEOS IN THE FOLDER WILL BE RESIZED",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")],
        initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/0) RAW videos"
    )
    
    if not file_path:
        root.destroy()
        return
    
    # Get the folder containing the selected file
    folder_path = os.path.dirname(file_path)
    
    # Get all files in the folder
    allfiles = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            allfiles.append(file_path)
    
    # Ask the user for the desired width
    width = simpledialog.askinteger("Input Width", "Enter the desired width (e.g., 1280):")
    if not width:
        print("No width provided. Exiting...")
        return
    elif width % 32 != 0:
        messagebox.showerror("ERROR", "Width MUST be a multiple of 32\nExamples: 1920, 1280, 1024, 480")
        return
    
    # Resize the videos and get the path to the resized folder
    resized_folder = resize_video_with_ffmpeg(allfiles, width, folder_path)
    
    # Open the folder containing the resized videos
    if resized_folder:
        open_folder(resized_folder)

if __name__ == "__main__":
    main()
