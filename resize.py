import os
import subprocess
from common.common import *

def resize_width(input_path,width:int,output_folder=None):
    """
    Resize a video's dimensions proportionally to a given width. Output
    
    Args:
        input_path (str): Path to the input video file.
        width (int): Desired width for the resized video. Must be a multiple of 32.The height will be adjusted proportionally.
        output_folder (str, optional): Path to the folder where the resized video will be saved. If not provided, the resized video will be saved in the same folder as the input video.

    Returns:
        str: Path to the resized video file.
    """
    # Get the directory and filename of the input video
    file_dir = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    while int(width) % 32 != 0:
        error("ERROR", "Width MUST be a multiple of 32\nExamples: 1920, 1280, 1024, 480")
        width = askint("Input Width", "Enter the desired width (must be a multiple of 32):",fill=width)

    if not output_folder:
        output_folder = file_dir
        output_path = os.path.join(output_folder, f"{file_name}-RESIZED{width}.mp4")
    else:
        output_path = os.path.join(output_folder, f"{file_name}.mp4")
    
    try:
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # NVIDIA GPU acceleration
            "-hwaccel_output_format", "cuda",  # Keep frames in GPU memory
            "-i", input_path,  
            "-vf", f"scale_cuda={width}:-2",  # Resize with proportional height
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            "-y",  # Overwrite output file if it exists
            "-an", # no audio
            output_path
        ]
        
        print("Starting video resizing...")
        subprocess.run(cmd, check=True)
        print(f"Resizing completed successfully! Resized video saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during resizing: {e}")
        return None


def main():
    
    file_paths = select_anyfile("Select video file(s) to resize", specific_ext="mp4")
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    # Ask the user for the desired width
    width = 1
    while width % 32 != 0:
        width = askint("Input Width", "Enter the desired width (e.g., 1280):")
        if not width:
            print("No width provided. Exiting...")
            return
        elif width % 32 != 0:
            error("ERROR", "Width MUST be a multiple of 32\nExamples: 1920, 1280, 1024, 480")

    for i, path in enumerate(file_paths):
        output_path = resize_width(path,width)
    clear_gpu_memory()
    # Open the folder containing the resized video
    if output_path:
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()
