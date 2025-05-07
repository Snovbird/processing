import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import platform
from tkinter import simpledialog

def apply_png_overlay(video_path, imgpath):
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
            "-i", imgpath,
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

def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select the input video file
    video_paths = filedialog.askopenfilenames(
        title="Select Input Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")],
        initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/"
    )
    
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    
    # Ask the user to select the PNG overlay image
    overlay_path = filedialog.askopenfilename(
        title="Select Transparent PNG Overlay",
        filetypes=[("PNG Files", "*.png")],
        initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/"
    )
    if False:
        cage_number = simpledialog.askinteger("Cage Number", 
                                            "Enter cage number (1,2,4,5,6,7,8,9,10,11,12):",minvalue=1,maxvalue=12)
        if not cage_number or int(cage_number) not in [1,2,4,5,6,7,8,9,10,11,12]:
            print("No overlay image selected. Exiting...")
            return
        width = simpledialog.askinteger("Width dimension", 
                                        "Enter width (2048, 1280, 1024, 480):",
                                            initialvalue=1024,  
                                            minvalue=480)
        if not width or int(width) not in [2048, 1024, 1280, 480]:
            print("No width selected. Exiting...")
            return
    
    # Apply the overlay to the video
    for vid in video_paths:
        output_path = apply_png_overlay(vid, overlay_path)
    
    if output_path:
        # Show a success message
        # messagebox.showinfo("Success", f"Video with overlay created successfully!/n/nSaved as: {os.path.basename(output_path)}")
        # Open the folder containing the output video
        print(output_path)
        os.startfile("C:/Users/Labo Samaha/Desktop/.LabGym/2) MARKED videos")
    else:
        # Show an error message
        messagebox.showerror("Error", "Failed to apply overlay. Check console for details.")

if __name__ == "__main__":
    main()