import os
import subprocess
from common.common import clear_gpu_memory,select_video,windowpath,askint,error,askstring,find_folder,find_value

def apply_png_overlay(video_path, cage_number,width,date,overlays_path,output_path):
    """
    Apply a transparent PNG overlay to a video using FFmpeg.
    
    Args:
        video_path (str): Path to the input video.
        cage_number (str): Path to the transparent PNG overlay.
    
    Returns:
        str: Path to the output video file.
    """
    # Get the directory and filename of the input video
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_path, f"{video_name}.mp4")
    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,
            "-i", os.path.join(overlays_path, f"{width}/cage{cage_number}_{date}_{width}.png"),
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
    # Ask the user to select the input video file
    startpath = windowpath()
    video_paths = select_video(title="Select Input Video(s) for ONE cage",path=startpath)
    
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    
    askforcage = True

    if askforcage:
        cage_number = askint("Cage Number", "Enter cage number (1,2,4,5,6,7,8,9,10,11,12):")
        if not cage_number or int(cage_number) not in [1,2,4,5,6,7,8,9,10,11,12]:
            print("No overlay image selected. Exiting...")
            return
    
    # width = simpledialog.askinteger("INPUT WIDTH", "What's the width of the video you're selecting?\n(ex: 2048, 1280, 1024, 480)",initialvalue=1024,minvalue=480)
    width = 2048
    if not width or int(width) not in [2048, 1024, 1280, 480]:
        print("No width selected. Exiting...")
        return
    
    # Apply the overlay to the video
    date = askstring(msg= "Enter the date formatted as MM-DD:", title="Enter Date",fill="06-")

    # Find 2) MAKRED VIDEOS folder
    output_path = find_folder("2) MARKED videos")
    overlays_path = find_folder("MARKERS_overlays")

    for vid in video_paths:
        output_path = apply_png_overlay(vid, cage_number, width,date,overlays_path,output_path)

    clear_gpu_memory()

    if output_path:
        # Show a success message
        # messagebox.showinfo("Success", f"Video with overlay created successfully!/n/nSaved as: {os.path.basename(output_path)}")
        # Open the folder containing the output video
        print(output_path)
        os.startfile("C:/Users/Labo Samaha/Desktop/.LabGym/2) MARKED videos")
    else:
        # Show an error message
        error(msg="Failed to apply overlay. Check console for details.")

if __name__ == "__main__":
    main()