import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import pyperclip
import wx
from common.common import clear_gpu_memory,custom_dialog

def apply_png_overlay(video_path, cage_number,width,where):
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
    output_path = os.path.join("C:/Users/Labo Samaha/Desktop/.LabGym/2) MARKED videos", f"{video_name}-marked.mp4")
    
    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,
            "-i", f"C:/Users/Labo Samaha/Desktop/.LabGym/z_misc_DONOTTOUCH/{width}{where}/cage{cage_number}-{width}{where}.png ",
            "-filter_complex", "[0][1]overlay=x=0:y=0",
            "-c:v", "h264_nvenc",
            "-y",  # Overwrite output file if it exists
            "-an",
            output_path
        ]
        print(" ".join(cmd))
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

def askfiles():
    try:
            video_paths = filedialog.askopenfilenames(
                title="Select Input Video (markersquick)",
                filetypes=[("Video Files", "*.mp4")],
                initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/"
            )
    except:
            video_paths = filedialog.askopenfilenames(
                title="Select Input Video",
                filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")])
    return video_paths

def main():
    # Initialize tkinter and hide the root window
    root = tk.Tk()
    root.withdraw()
    folderpath = pyperclip.paste()
    if os.path.isdir(folderpath):
        video_paths = []
        count = 0
        filesinside = os.listdir(folderpath)
        for file in filesinside:
            count +=1
            if os.path.splitext(file)[1] in ['.mp4']: #'.avi','.mov.','.webm','.mkv']: # is file extension the right one
                video_paths.append(os.path.join(folderpath,file))
            elif count == len(filesinside):
                video_paths = askfiles()
    else:
        video_paths = askfiles()
    # Ask the user to select the input video file
        
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    
    AL_position = custom_dialog(None, title="Active lever position", message="Is the active lever near the door (FN) or away (FF)", option1="FN", option2="FF")
    
    # width = simpledialog.askinteger("INPUT WIDTH", "What's the width of the video you're selecting?\n(ex: 2048, 1280, 1024, 480)",initialvalue=1024,minvalue=480)
    width = 2048
    if not width or int(width) not in [2048, 1024, 1280, 480]:
        return

    for vid in video_paths:
        for i in range(12):
            if len(str(12-i)) == 2 and str(12-i) in vid.split("/")[-1].replace(".mp4",""):
                    print(vid.split("/")[-1].replace(".mp4",""))
                    output_path = apply_png_overlay(vid, 12-i, width,AL_position)
                    break
            elif str(12-i) in vid.split("/")[-1].replace(".mp4",""): 
                output_path = apply_png_overlay(vid, 12-i, width,AL_position)
    if output_path:
        print(output_path)
        clear_gpu_memory()
        os.startfile("C:/Users/Labo Samaha/Desktop/.LabGym/2) MARKED videos")
    else:
        # Show an error message
        messagebox.showerror("Error", "Failed to apply overlay. Check console for details.")

if __name__ == "__main__":
    main()