import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
import platform

def overlay_FRAMES(input_path,folder_path = None):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    
    Args:
        input_path (str): Path to the input video file.
        width (int): Desired width for the resized video.
    
    Returns:
        str: Path to the resized video file.
    """
    # Get the directory and filename of the input video
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    if folder_path:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(folder_path, f"{file_name}-overlaid.mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}-overlaid.mp4")
    
    try:
        # FFmpeg command to OVERLAY frames
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-i", input_path,  # Input file
            "-vf", "drawtext=fontfile=Arial.ttf:text=%{n}:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768",  # overlay
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            "-y",  # Overwrite output file if it exists
            "-an", #no audio stream output
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

def makefolder(file_path):
    # Get directory containing the file
    folder_path = os.path.dirname(file_path)
    
    # Get just the filename without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create folder name
    resized_folder_name = f"{file_name}-overlaid"
    
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
    answer = 'no'
    if len(file_paths) > 1:
        answer = messagebox.askquestion("Question", "Create New Folder?")
        if answer == 'yes':
            folder_path = makefolder(file_paths[0])
    # overlay frame number
    if len(file_paths) > 1 and answer == 'yes':
        for i, path in enumerate(file_paths):
            if i > 0:
                # Clear GPU memory between files
                pass
            output_path = overlay_FRAMES(path, folder_path)
    else:
        for i, path in enumerate(file_paths):
            if i > 0:
                # Clear GPU memory between files
                pass
            output_path = overlay_FRAMES(path)
    clear_gpu_memory()
    root.destroy()
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
