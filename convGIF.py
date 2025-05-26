import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import platform
from tkinter import simpledialog

def apply_png_overlay(video_path,frame_rate):
    """
    Convert to GIF
    """
    # Get the directory and filename of the input video
    video_dir = os.path.dirname(video_path)
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(video_dir, f"{video_name}.gif")
    
    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",                # Use NVIDIA GPU for hardware acceleration
            "-hwaccel_output_format", "cuda",
            "-c:v", "h264_cuvid",              # Use NVIDIA decoder for input
            "-i", video_path,                  # Input file path
            "-filter_complex", f"fps={frame_rate},scale=-1:480[s]; [s]split[a][b]; [a]palettegen[palette]; [b][palette]paletteuse",  # Create optimal color palette
            "-y",                              # Overwrite output without asking
            output_path                        # Output GIF path
        ]

        
        print("Starting to convert to gif...")
        subprocess.run(cmd, check=True)
        print(f"Overlay completed successfully! Output saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during overlay process: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

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
    
def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select the input video file
    try:
        video_paths = filedialog.askopenfilenames(
            title="Select Input Video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")],
            initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/"
        )
    except:
        video_paths = filedialog.askopenfilenames(
            title="Select Input Video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")])
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    
    frame_rate = simpledialog.askinteger("Frame rate", 
                                            "Enter frame rate (1-15):",minvalue=1,maxvalue=12)

    for i, vid in enumerate(video_paths):
        if i > 0:
            # Clear GPU memory between files
            pass
        output_path = apply_png_overlay(vid, frame_rate)
    clear_gpu_memory()
    if output_path:
        # Show a success message
        # messagebox.showinfo("Success", f"Video with overlay created successfully!/n/nSaved as: {os.path.basename(output_path)}")
        # Open the folder containing the output video
        print(output_path)
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()