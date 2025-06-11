import subprocess
import os


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

def overlay_FRAMES(input_path,folder_path = None):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    
    Args:
        input_path (str): Path to the input video file.
        width (int): Desired width for the resized video.
    
    Returns:
        str: Path to the resized video file.
    """
    # Get the directory and filename of the input video
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    if folder_path:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(folder_path, f"{file_name}-overlaid.mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}-overlaid.mp4")
    
    try:
        # FFmpeg command to OVERLAY frames
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",  # Use NVIDIA GPU acceleration
            "-i", input_path,  # Input file
            "-vf", "drawtext=fontfile=Arial.ttf:text=%{n}:x=(w-tw)/2:y=(h-th)/2:fontcolor=white:box=1:boxcolor=0x00000000:fontsize=h*16/768",  # overlay
            "-c:v", "h264_nvenc",  # Use NVIDIA H.264 encoder
            "-y",  # Overwrite output file if it exists
            "-an", #no audio stream output
            output_path
        ]
        
        print("Starting video resizing...")
        subprocess.run(cmd, check=True)
        print(f"Resizing completed successfully! Resized video saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during resizing: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def trim_video_timestamps_accelerated(input_path, start_time, end_time, count, foldername=None):
    startforname = start_time.replace(":", "")
    endforname = end_time.replace(":", "")
    
    # Create unique output path for each segment
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, f"{file_name}-trim({startforname}-{endforname}).mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}-trim({startforname}-{endforname}).mp4")
    
    try:
        # GPU-accelerated command for a single segment
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-c:v", "h264_cuvid",
            "-i", input_path,
            "-ss", start_time,
            "-to", end_time,
            "-c:v", "h264_nvenc",
            "-preset", "p1",
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)    
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None

def trim_frames(input_path, start_time, end_time,count,foldername=None):
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, f"{file_name}-trim({start_time}-{end_time}).mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}-trim({start_time}-{end_time}).mp4")

    try:
        cmd = [

            "ffmpeg", 
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-c:v", "h264_cuvid",
            "-i", input_path, 
            "-vf", f'trim=start_frame={start_time}:end_frame={end_time},setpts=PTS-STARTPTS', 
            "-c:v", "h264_nvenc",  
            "-preset", "p1",
            "-af", f'aresample=async=1',        
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd), "\n*****************************************************************************************************")
        subprocess.run(cmd, check=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not on PATH.")
        return None











