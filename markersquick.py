import os
import subprocess
from common.common import clear_gpu_memory,askstring,select_video,windowpath,find_folder_path,findval,error,assignval,makefolder
import sys
def apply_png_overlay(video_path, output_path,cage_number,thedate,overlays_path):
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

    output_path = os.path.join(output_path, f"{video_name}_{cage_number}.mp4")

    alldates = findval("dates")[::-1]
    for d in range(alldates.index(thedate),len(alldates)):
        imagepath = os.path.join(overlays_path, f"cage{cage_number}_{alldates[d]}.png") # f"{width}/cage{cage_number}_{alldates[d]}_{width}.png")
        if os.path.exists(imagepath):
            break
    else: # redundant but idc
        if not os.path.exists(imagepath):
            error(msg=f"There is no overlay images for cage {cage_number}.\nPath '{imagepath}' does not exist")
            return "Error: No overlay png"
    center = True
    center = False
    
    if center:
        drawtext = "drawtext=fontfile=Arial.ttf:text=%{n}:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768"
    else: # top left corner
        drawtext ="drawtext=fontfile=Arial.ttf:text=%{n}:x=(0)/2:y=(0)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768"

    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,
            "-i", imagepath,
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

def main():
    # Initialize tkinter and hide the root window
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
    video_paths = select_video(title="Select videos for MARKERS QUICK",path=startpath)

    if not video_paths:
        print("No video file selected. Exiting...")
        return
    thedate = askstring(msg= "Enter the date formatted as MM-DD:", title="Enter Date",fill=findval("last_used_date"))
    assignval("last_used_date",thedate)

    # AL_position = custom_dialog(title="Active lever position", msg="Is the active lever near the door (FN) or away (FF)", op1="FN", op2="FF")
    
    width = 2048
    if not width or int(width) not in [2048, 1024, 1280, 480]:
        return
    

    from datetime import date
    # Get today's date
    today = date.today()
    # Format the date as MM-DD
    formatted_date = today.strftime("%m-%d")
    alldates = findval("dates")
    if alldates[-1] != formatted_date:
        alldates.append(formatted_date)
        assignval("dates",alldates)
        print(f"Added date: {formatted_date}")

    # Find output folder named "2) MARKED videos"
    # output_path = find_folder("2) MARKED videos")
    
    output_path = makefolder(video_paths[0],foldername="marked-") # Unless I want to add a suffix like "-marked" to all videos, the output folder is necessary so the output has exact same name as input 

    overlays_path = find_folder_path("2-MARKERS") # Contains image overlays
    for vid in video_paths:
        cage_number = ''.join(char for char in os.path.splitext(os.path.basename(vid))[0][0:2] if char.isdigit()) # [0:2] since only the first 2 numbers interest us
        output_vid_path = apply_png_overlay(vid, output_path=output_path,cage_number=cage_number,thedate=thedate,overlays_path=overlays_path,) 

    if output_vid_path:
        print(output_vid_path)
        clear_gpu_memory()
        os.startfile(output_path)
    else:
        # Show an error message
        
        error("Error", "Failed to apply overlay. Check console for details.")

if __name__ == "__main__":
    main()
    