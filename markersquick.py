import os
import subprocess
from common.common import *
import sys
from common.exceptions import *

def find_overlay_path(img_path, room=None) -> str:
    """
    Args:
        img_path (str): full png image path where basename is formatted as `01-20251022.png` or `01-20251022-018010-3080.png`, which is nn-YYYYMMDD-HHMMSS-HHMMSS.png (nn = cage number, uses zfill to make sure it is 2 digits)
        room (str): room folder name in 2-markers
    """
    basename = os.path.splitext(os.path.basename(img_path))[0]
    parts = basename.split("-")
    
    if not parts or len(parts) < 2:
        raise ValueError(f"Invalid image path format: {img_path}")
        
    cage_number = parts[0].zfill(2)
    date_provided = parts[1]
    
    img_starttime = None
    if len(parts) >= 3 and parts[2].isdigit():
        img_starttime = int(parts[2]) 

    markers_folder = find_folder_path("2-markers")

    if not room:
        room = simple_dropdown(title="Select Room", msg="Select the room for the overlay:", choices=[i for i in list_folders(markers_folder) if "template" not in i.lower()])
    overlay_path = os.path.join(markers_folder, room)

    # Gather all overlays for this cage
    all_overlays = list_filespaths(overlay_path)
    overlays_for_cage = [ov for ov in all_overlays if os.path.basename(ov).split("-")[0].zfill(2) == cage_number]
    overlays_for_cage.sort(reverse=True)
    
    overlays_for_cage_per_date = {}
    for ov in overlays_for_cage:
        date = os.path.splitext(os.path.basename(ov))[0].split("-")[1]
        overlays_for_cage_per_date[date] = overlays_for_cage_per_date.get(date, []) + [ov] # if only one overlay for this date: 

    
    if not overlays_for_cage:
        raise ImageNotFoundError(f"No overlays found for cage {cage_number} in room {room}")

    # find overlay closest to provided date and time (if provided)
    fallback_overlay = None

    dates = list(overlays_for_cage_per_date.keys())
    dates.sort(reverse=True)
    
    for n,ov_date in enumerate(dates):
        previous_date = dates[n+1] if n+1 < len(dates) else None
        if ov_date == date_provided:
            number_of_overlays_for_date = len(overlays_for_cage_per_date[ov_date])
            if not img_starttime:
                overlay_path = overlays_for_cage_per_date[ov_date][-1]
                return overlay_path # least recent for the date (shouldn't have a start time)
            elif number_of_overlays_for_date > 1:
                for n,ov_path in enumerate(overlays_for_cage_per_date[date]):
                    ov_basename = os.path.splitext(os.path.basename(ov_path))[0]
                    ov_parts = ov_basename.split("-") # 01-20250925-100000
                    ov_start = int(ov_parts[2])
                    if ov_start > img_starttime: # if the image provided is older than the most recent item
                        continue
                    else:
                        if n + 1 > (number_of_overlays_for_date-1): # reminder: n starts at 0, but length starts at 1 item
                            return ov_path # there is no previous overlay for this date
                        else:
                            next_ov_path = overlays_for_cage_per_date[ov_date][n+1]
                            next_ov_basename = os.path.splitext(os.path.basename(next_ov_path))[0]
                            next_ov_parts = next_ov_basename.split("-") # 01-20250925-100000
                            next_ov_start = int(next_ov_parts[2])
                            if next_ov_start < img_starttime:
                                return next_ov_path
            elif number_of_overlays_for_date == 1:
                overlay_path = overlays_for_cage_per_date[ov_date][0]
                return overlay_path
        elif previous_date and previous_date < date_provided < ov_date:
            return overlays_for_cage_per_date[previous_date][0] # most recent overlay before provided date
        elif ov_date < date_provided:
            return overlays_for_cage_per_date[ov_date][0] # most recent overlay before provided date
    else:
        raise ImageNotFoundError(f"No overlay found for cage {cage_number} on {date_provided}" + (f" at {img_starttime}" if img_starttime else '') + f"\n Image path: {img_path}")

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

        if cage_number and date_to_provide:
            mock_basename = f"{cage_number}-{date_to_provide}"
            overlay_path = find_overlay_path(mock_basename, room)
        else:
            overlay_path = find_overlay_path(video_name, room)

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