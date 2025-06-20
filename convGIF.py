import os
import subprocess
from common.common import clear_gpu_memory,select_video,windowpath,custom_dialog,makefolder,msgbox

def conv_gif(video_path,frame_rate,outputfolder=None):
    """
    Convert to GIF
    """
    if not outputfolder:
        outputfolder = os.path.dirname(video_path)
    # Get the directory and filename of the input video
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(outputfolder, f"{video_name}.gif")
    temp_path = os.path.join(outputfolder, "temp_output.mkv")
    
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
        return os.path.dirname(output_path)
    
    except subprocess.CalledProcessError as e:
        print(f"Error during overlay process: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None
    
def main():
    startpath = windowpath()    
    # Ask the user to select the input video file
    video_paths = select_video(title="Select videos to convert to gif",path=startpath)
    if not video_paths:
        print("No video file selected. Exiting...")
        return
    if custom_dialog("Make output FOLDER?") == 'yes':
        outputfolder = makefolder(video_paths[0],"Gifs")
    else:
        outputfolder = None
    frame_rate = None
    # frame_rate = simpledialog.askstring("Frame rate", 
    #                                         "Enter frame rate (1-12):",minvalue=1,maxvalue=12)
    if not frame_rate:
        frame_rate = 12

    for i, vid in enumerate(video_paths):
        output_path = conv_gif(vid, frame_rate,outputfolder)


    clear_gpu_memory()
    if output_path:
        msgbox(f"Video with overlay created successfully!/n/nSaved as: {os.path.basename(output_path)}","Success")
        # Open the folder containing the output video
        os.startfile(os.path.dirname(output_path))

if __name__ == "__main__":
    main()