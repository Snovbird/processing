import subprocess
import tempfile
import os
from common.common import select_video,askint,windowpath,clear_gpu_memory,makefolder

def combine_videos_with_cuda(input_files,output_folder):
    """
    Combine multiple video files using NVIDIA CUDA hardware acceleration.
    
    Args:
        input_files (list): List of paths to input video files in desired order
        output_file (str): Path to the output video file
        video_bitrate (str): Video bitrate for encoding
        preset (str): NVENC encoding preset (p1-p7)
    """
    # Create a temporary file for the concat list
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
        for file in input_files:
            # Escape single quotes in filenames and use absolute paths
            escaped_file = os.path.abspath(file).replace("'", "'\\''")
            temp.write(f"file '{escaped_file}'\n")
        temp_filename = temp.name

    outputfile = f'concat{os.path.basename(input_files[0])}'
    output = os.path.join(output_folder,outputfile)

    try:
        # Build the ffmpeg command
        cmd = [
            'ffmpeg',
            '-y',                          # Overwrite output file if it exists
            '-hwaccel', 'cuda',            # Use CUDA for decoding
            '-hwaccel_output_format', 'cuda',  # Keep frames in GPU memory
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_filename,
            '-c:v', 'h264_nvenc',          # Use NVIDIA hardware encoder
            '-preset', 'p1', #preset,
            # '-b:v', video_bitrate,
            '-an',                
            output
        ]
        print(cmd)
        # Run the command with error checking
        subprocess.run(cmd, check=True)
        return True
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def main():
    startpath = windowpath()
    number_of_concats = askint(title="Output number",msg='How many concatenations to do?')
    toconcat = [select_video(title="select videos to concatenate first",path=startpath) for c in range(number_of_concats)]
    output_folder = makefolder(toconcat[0][0],foldername='concat')

    for setofvids in toconcat:
        ready = combine_videos_with_cuda(setofvids,output_folder)
    if ready:
        clear_gpu_memory()
        os.startfile(output_folder)

# Example usage
if __name__ == "__main__":
    main()
