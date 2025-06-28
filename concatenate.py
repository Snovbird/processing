import subprocess
import tempfile
import os
from common.common import select_video,askint,clear_gpu_memory,makefolder
import sys


def combine_videos_with_cuda(input_files, output_folder):
    if True or len(input_files) > 2:
        """
        Combine multiple video files using NVIDIA CUDA hardware acceleration with two-stage approach.
        """
        # Create intermediate directory for temporary files
        temp_dir = tempfile.mkdtemp()
        intermediate_files = []
        
        try:
            # STAGE 1: Transcode each file to ensure consistency
            for i, file in enumerate(input_files):
                temp_output = os.path.join(temp_dir, f"temp_{i}.mp4")
                intermediate_files.append(temp_output)
                
                # Each file processed individually with CUDA
                cmd = [
                    'ffmpeg', '-y',
                    '-hwaccel', 'cuda',
                    '-i', file,
                    '-c:v', 'h264_nvenc',
                    '-preset', 'p1',
                    '-an',  # No audio
                    temp_output
                ]
                subprocess.run(cmd, check=True)
            
            # STAGE 2: Concatenate the uniformly encoded files
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
                for file in intermediate_files:
                    escaped_file = os.path.abspath(file).replace("'", "'\\''")
                    temp.write(f"file '{escaped_file}'\n")
                concat_list = temp.name
            
            outputfile = f'concat{os.path.basename(input_files[0])}'
            output = os.path.join(output_folder, outputfile)
            
            # Simple concatenation of consistently encoded files (no CUDA needed for this stage)
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_list,
                '-c', 'copy',  # Just copy streams without re-encoding
                output
            ]
            subprocess.run(cmd, check=True)
            return True
            
        finally:
            # Clean up all temporary files
            for file in intermediate_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except:
                        pass
            if os.path.exists(concat_list):
                os.remove(concat_list)
            try:
                os.rmdir(temp_dir)
            except:
                pass
    elif False and len(input_files) == 2:
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
                '-vf', 'hwupload_cuda,scale_cuda=format=nv12',
                '-c:v', 'h264_nvenc',          # Use NVIDIA hardware encoderAdd commentMore actions
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
        user_profile = os.environ['USERPROFILE']
        downloads_folder = os.path.join(user_profile, 'Downloads')

        with open(os.path.join(downloads_folder, f"error.txt"),'a') as f:
            f.write(str(e) + '\n')
            f.write('-'*35 + '\n')
            print(str(e))
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
