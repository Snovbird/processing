import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import platform
from tkinter import simpledialog
from common.common import clear_gpu_memory

def conv_gif(video_path,frame_rate):
    """
    Convert to GIF
    """
    # Get the directory and filename of the input video
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(video_dir, f"{video_name}.gif")
    temp_path = os.path.join(video_dir, "temp_output.mkv")
    
    try:
        # Step 1: Decode with hardware acceleration to a temporary file with a lossless codec
        step1_cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-c:v", "h264_cuvid",
            "-i", video_path,
            "-c:v", "ffv1",  # Lossless codec
            "-y",
            temp_path
        ]

        # Step 2: Create GIF from the intermediate file
        step2_cmd = [
            "ffmpeg",
            "-i", temp_path,
            "-vf", f"fps={frame_rate},scale=-1:768,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
            "-y",
            output_path
        ]






        
        print("Starting to convert to gif...")
        subprocess.run(step1_cmd, check=True)
        subprocess.run(step2_cmd, check=True)
        print(f"Overlay completed successfully! Output saved to: {output_path}")
        os.remove(temp_path)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during overlay process: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None
    
def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select the input video file
    video_paths = filedialog.askopenfilenames(
        title="Select Input Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")])
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    frame_rate = None
    # frame_rate = simpledialog.askstring("Frame rate", 
    #                                         "Enter frame rate (1-12):",minvalue=1,maxvalue=12)
    if not frame_rate:
        frame_rate = 12
    for i, vid in enumerate(video_paths):
        if i > 0:
            # Clear GPU memory between files
            pass
        output_path = conv_gif(vid, frame_rate)
    clear_gpu_memory()
    if output_path:
        # Show a success message
        # messagebox.showinfo("Success", f"Video with overlay created successfully!/n/nSaved as: {os.path.basename(output_path)}")
        # Open the folder containing the output video
        print(output_path)
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()