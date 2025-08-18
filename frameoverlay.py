import os
import subprocess
import platform
from common.common import clear_gpu_memory,select_video,makefolder,custom_dialog,windowpath,select_anyfile

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

    center = True
    center = False
    
    if center:
        drawtext = "drawtext=fontfile=Arial.ttf:text=%{n}:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768"
    else: # top left corner
        drawtext ="drawtext=fontfile=Arial.ttf:text=%{n}:x=(0)/2:y=(0)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768"
    try:
        # FFmpeg command to OVERLAY frames
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-i", input_path,  # Input file
            "-vf", drawtext,  # overlay
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

def main():
    import sys
    # Check if a startpath was provided
    if len(sys.argv) > 1:
        path_arg = sys.argv[1]
        # Check if the argument is a valid directory path
        if os.path.isdir(path_arg):
            startpath = path_arg
        else:
            # If not a full path, try to construct one from common locations
            possible_paths = [
                os.path.join(os.path.expanduser("~"), path_arg),      # User folder
                os.path.join(os.path.expanduser("~"), "Desktop", path_arg), # Desktop
                os.path.join("C:\\", path_arg)                       # Root drive
            ]
            for path in possible_paths:
                if os.path.isdir(path):
                    startpath = path
                    break
    else:
        startpath = ''

    # Ask the user to select a video file
    file_paths = select_anyfile(
        title="Select one Video File",
        path=startpath
    )
    if not file_paths:
        print("No file selected. Exiting...")
        return
    answer = None
    if len(file_paths) > 1:
        answer = custom_dialog("Question", "Create New Folder?")
        if answer == 'yes':
            folder_path = makefolder(file_paths[0],foldername='overlaid')
    # overlay frame number
    if answer == 'yes':
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
    # Open the folder containing the resized video
    if output_path:
        os.startfile(os.path.dirname(output_path))
    
if __name__ == "__main__":
    main()
