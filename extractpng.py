import subprocess
import os
from common.common import clear_gpu_memory,select_video,askstring,makefolder,windowpath,hhmmss_to_seconds

def extractpng(video: str, times: list[int], output_folder: str):
    """
    Extracts frames from a video at specific timestamps using ffmpeg's fast seek.

    Args:
        video (str): Path to the input video file.
        times (list[int]): A list of timestamps in seconds to extract frames from.
        output_folder (str): The folder to save the extracted PNG frames.
    """
    video_name = os.path.splitext(os.path.basename(video))[0]
    for i, seconds in enumerate(times):
        # Create a unique filename for each frame from each video to avoid overwrites
        output_filename = os.path.join(output_folder, f'{video_name}_{i:03d}.png')

        # This command uses fast seeking (-ss before -i) which is very efficient
        # for extracting individual frames without decoding the whole video.
        # GPU acceleration is omitted here as the overhead for starting it for each
        # frame often makes it slower than CPU-based seeking for this task.
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            '-ss', str(seconds),  # Seek to the desired timestamp
            '-i', video,
            '-frames:v', '1',  # Extract only one frame
            '-q:v', '1',  # High quality PNG
            output_filename
        ]

        print(f"Extracting frame from '{os.path.basename(video)}' at {seconds}s...")
        try:
            # Using capture_output=True to hide ffmpeg's verbose output unless there's an error
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error extracting frame at {seconds}s from {os.path.basename(video)}")
            print(f"FFmpeg stderr: {e.stderr}")

def main():
    import sys
    try:
        # Get argument
        startpath = sys.argv[1]
        
        # If the path doesn't exist as-is, try to construct a proper path
        if not os.path.isdir(startpath):
            # Try to match with common Windows folders
            possible_paths = [
                os.path.join(os.path.expanduser("~"), startpath),  # User folder
                os.path.join(os.path.expanduser("~"), "Desktop", startpath),    # Desktop
                os.path.join("C:\\", startpath)  # Root drive
            ]
            
            for path in possible_paths:
                if os.path.isdir(path):
                    startpath =  path
                    break

    except Exception as e:
        startpath = ''

    
    videos = select_video(title="Videos to extract frames from",path=startpath)

    if not videos:
        return
    time_str = askstring(title='Times',msg="Enter HHMMSS times separated by a period (.):")
    if not time_str:
        return

    # Use the robust hhmmss_to_seconds function from common and filter out empty strings
    times = [hhmmss_to_seconds(t) for t in time_str.split('.') if t]
    if not times:
        return
    output_folder = makefolder(videos[0],"PNG-")
    for video in videos:
        extractpng(video,times,output_folder)
    clear_gpu_memory()
    os.startfile(os.path.dirname(videos[0]))
    

if __name__ == '__main__':
    main()
