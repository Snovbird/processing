import os
import subprocess
from common.common import *
import sys
from common.exceptions import *

def find_overlay_path(date_provided:str=None,room:str=None,cage_number:int | str=None,img_path_optional=None) -> str:
    """
    Args:
        date_provided (str): date as YYYYMMSS 
        room (str): specific room name. Should be listed inside of `2-markers` folder
        cage_number (int | str): cage number. Will be converted to dual digit string (ex: `02`)
        img_path_optional (str): if `date_provided`, `room` and `cage_number` are None, will extract these values from file basename as 01-20251022 and room will be 
    
    """
    cage_number = str(cage_number).zfill(2)
    overlays_path = find_folder_path("2-markers")
    alldates = findval("dates")[::-1] # invert it to loop from latest dates first then to earlier ones
    if date_provided not in alldates:
        for date in alldates: 
            if int(date) < int(date_provided): #get img from date right before
                overlay_path = os.path.join(overlays_path, room, f"{cage_number}-{date}.png")
                if os.path.exists(overlay_path):
                    break
        else:
            raise ImageNotFoundError(f"No overlays for cage {cage_number} on {date_provided} in room {room}")
    else:
        for date_index in range(alldates.index(date_provided),len(alldates)):
            overlay_path = os.path.join(overlays_path, room,f"{cage_number}-{alldates[date_index]}.png") # f"{width}/cage{cage_number}_{alldates[d]}_{width}.png")
            if os.path.exists(overlay_path):
                break
        else:
            raise ImageNotFoundError(f"No overlays for cage {cage_number} on {date_provided} in room {room}")
    return overlay_path


def apply_png_overlay(video_path, output_folder,overlay_path= None,room="OPTO-ROOM (12 cages)",cage_number=None,date_to_provide=None):
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

    output_path = os.path.join(output_folder, f"{video_name}.mp4")
    overlays_path = find_folder_path("2-markers")
    if not overlay_path:
        if not cage_number:
            cage_number = ''.join(char for char in video_name[0:2] if char.isdigit()) 

        if not date_to_provide: # If a date is inside of the video name,but today's date was not provided (date_today = today's date)
            
            date_to_provide = video_name.split("-")[1]
            if not is_date(date_to_provide):
                date_to_provide = findval("dates")[-1] # will loop through known dates
        #today's date was provided
        overlay_path = find_overlay_path(date_to_provide,room,cage_number)

        # no matter what check if image works
        if not os.path.exists(overlay_path):
            error(msg=f"There is no overlay images for cage {cage_number}.\nPath '{overlay_path}' does not exist")
            return "Error: No overlay png"

    try:
        # FFmpeg command to overlay the PNG on the video using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,
            "-i", overlay_path,
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
    
    output_folder = makefolder(video_paths[0],foldername="marked_videos")

    if custom_dialog("Find overlays automatically?","Overlay selection",raiseerror=True) == "no":
        date_provided = askstring(msg= "Enter the date formatted as MM-DD:", title="Enter Date",fill=findval("last_used_date"))
        assignval("last_used_date",date_provided)
        width = 2048
        if not width or int(width) not in [2048, 1024, 1280, 480]:
            return
    
         # Unless I want to add a suffix like "-marked" to all videos, the output folder is necessary so the output has exact same name as input 
    
        for vid in video_paths:
            cage_number = ''.join(char for char in os.path.splitext(os.path.basename(vid))[0][0:2] if char.isdigit()) # [0:2] since only the first 2 numbers interest us
            output_vid_path = apply_png_overlay(vid, output_folder=output_folder,cage_number=cage_number,date_to_provide=date_provided) 
    else:
        for vid in video_paths:
            output_vid_path = apply_png_overlay(vid, output_folder=output_folder)
    if output_vid_path:
        print(output_vid_path)
        clear_gpu_memory()
        os.startfile(output_folder)
    else:
        # Show an error message
        error("Error", "Failed to apply overlay. Check console for details.")

    
if __name__ == "__main__":
    main()