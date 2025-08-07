import subprocess
import tempfile
import os
from common.common import select_video,askint,clear_gpu_memory,makefolder,custom_dialog,select_folder,error
import sys


def concatenate(input_files:list[str], output_folder:str):
    if True or len(input_files) > 2:
        """
        Combine multiple video files using NVIDIA CUDA hardware acceleration with two-stage approach.
        """
        # Create intermediate directory for temporary files
        temp_dir = tempfile.mkdtemp()
        intermediate_files = []
        concat_list_txt = None
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
                concat_list_txt = temp.name
            
            basename,ext = os.path.splitext(os.path.basename(input_files[0]))
            date = basename.split("_")[1]
            output_name = f"{''.join(char for char in basename[0:2] if char.isdigit())}_{date}{ext}" # Output should be named after the cage number
            output_path = os.path.join(output_folder, output_name)
            
            # Simple concatenation of consistently encoded files (no CUDA needed for this stage)
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_list_txt,
                '-c', 'copy',  # Just copy streams without re-encoding
                output_path
            ]
            print(cmd)
            try:
                subprocess.run(cmd, check=True)
            except:
                error(f"error with {input_files}")
            return output_path
            
        finally:
            # Clean up all temporary files
            for file in intermediate_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except:
                        pass
            if os.path.exists(concat_list_txt):
                os.remove(concat_list_txt)
            try:
                os.rmdir(temp_dir)
            except:
                pass
    # elif False and len(input_files) == 2:
    #     """
    #     Combine multiple video files using NVIDIA CUDA hardware acceleration.
        
    #     Args:
    #         input_files (list): List of paths to input video files in desired order
    #         output_file (str): Path to the output video file
    #         video_bitrate (str): Video bitrate for encoding
    #         preset (str): NVENC encoding preset (p1-p7)
    #     """
    #     # Create a temporary file for the concat list
    #     with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp:
    #         for file in input_files:
    #             # Escape single quotes in filenames and use absolute paths
    #             escaped_file = os.path.abspath(file).replace("'", "'\\''")
    #             temp.write(f"file '{escaped_file}'\n")
    #         temp_filename = temp.name

    #     outputfile = f'concat{os.path.basename(input_files[0])}'
    #     output = os.path.join(output_folder,outputfile)

    #     try:
    #         # Build the ffmpeg command
    #         cmd = [
    #             'ffmpeg',
    #             '-y',                          # Overwrite output file if it exists
    #             '-hwaccel', 'cuda',            # Use CUDA for decoding
    #             '-hwaccel_output_format', 'cuda',  # Keep frames in GPU memory
    #             '-f', 'concat',
    #             '-safe', '0',
    #             '-i', temp_filename,
    #             '-vf', 'hwupload_cuda,scale_cuda=format=nv12',
    #             '-c:v', 'h264_nvenc',          # Use NVIDIA hardware encoderAdd commentMore actions
    #             '-preset', 'p1', #preset,
    #             # '-b:v', video_bitrate,
    #             '-an',              
    #             output
    #         ]
    #         print(cmd)
    #         # Run the command with error checking
    #         subprocess.run(cmd, check=True)
    #         return True
        
    #     finally:
    #         # Clean up the temporary file
    #         if os.path.exists(temp_filename):
    #             os.remove(temp_filename)

def main():
    startpath = None
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
        pass # File explorer is not focused
        # error(str(e))
        # startpath = ''
        # user_profile = os.environ['USERPROFILE']
        # downloads_folder = os.path.join(user_profile, 'Downloads')

        # with open(os.path.join(downloads_folder, f"error.txt"),'a') as f:
        #     f.write(str(e) + '\n')
        #     f.write('-'*35 + '\n')
        #     print(str(e))
    if startpath is None:
        startpath = select_folder()
    elif not os.path.isdir(startpath):
        startpath = select_folder()
    # number_of_concats = askint(title="Output number",msg='How many concatenations to do?')
    # toconcat = [select_video(title="select videos to concatenate first",path=startpath) for c in range(number_of_concats)]
    files = [file for file in os.listdir(startpath) if os.path.isfile(os.path.join(startpath, file))]
    toconcat = group_files_by_digits(files)
    # Format the groups for display to fix the syntax and a potential type error.
    display_string = "\n\n".join([", ".join(group) for group in toconcat])
    check = custom_dialog(msg=f"Are these the expected groups: \n\n{display_string}",title="Verification",dimensions=(500,600))
    toconcat = [[os.path.join(startpath,file) for file in group] for group in toconcat]

    
    if check != 'yes':
        return
    output_folder = makefolder(toconcat[0][0],foldername='concat')
    for setofvids in toconcat:
        ready = concatenate(setofvids,output_folder)
    if ready:
        clear_gpu_memory()
        os.startfile(output_folder)

def group_files_by_digits(file_paths: list[str]) -> list[list[str]]:
    from collections import defaultdict

    """
    Groups a list of file paths based on the digits in their filenames.

    For example, 'cage8_partA.mp4' and 'cage8_partB.mp4' would be grouped
    together because their digit-key is '8'.

    Args:
        file_paths: A list of full file paths.

    Returns:
        A list of lists, where each inner list contains file paths
        that have the same sequence of digits in their names.
    """
    # A defaultdict makes it easy to append to lists without checking if the key exists.
    grouped_files = defaultdict(list)

    for file_path in file_paths:
        # Get just the filename from the full path
        filename = os.path.basename(file_path)
        
        # Extract the filename without the extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # This is your provided logic to create the grouping key
        digit_key = ''.join([char for char in name_without_ext if char.isdigit()])
        
        # Add the full file path to the list for this key
        grouped_files[digit_key].append(file_path)
        
    # We only need the lists of grouped files, not the keys themselves.
    # We also filter out any "groups" that only contain a single file.
    return [group for group in grouped_files.values() if len(group) > 1]

# Example usage
if __name__ == "__main__":
    main()
