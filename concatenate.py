import subprocess
import tempfile
import os,shutil,sys
from common.common import select_video,askint,clear_gpu_memory,makefolder,custom_dialog,select_folder,error


def concatenate(input_files:list[str], output_folder:str) -> str | None:
    """
    Example video output basename: `11-20250925.mp4` (removes times)
    Args:
        input_files (list): Array of mp4 video files paths to concatenate if 2+ items. If single item in array: moves to output_folder (concatenation skipped)
        output_folder: where concatenated videos are stored
    Returns:
        output_path: path to the concatenated video file (`None` if single item in array)
    """
    if len(input_files) > 2:
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
            cage, date, *_ = basename.split("-")
            output_name = f"{cage}-{date}{ext}" # Output should be named after the cage number
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
            print(f"{'CONCATENATE':^40}")
            print(cmd)
            subprocess.run(cmd, check=True)
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
    else: # move to output folder if single item in group
        if len(input_files) == 0:
            error("Empty array of input files for concatenation. Skipping...","Simple warning")
            return None
        filepath = input_files[0]
        name,ext = os.path.splitext(os.path.basename(filepath))
        folder = os.path.dirname(filepath)
        cage,date, *_ = name.split("-")
        newpathname = os.path.join(folder,f"{cage}-{date}{ext}")
        os.rename(filepath,newpathname)
        if output_folder != os.path.dirname(filepath):
            moved_path = shutil.move(newpathname, output_folder)
            return moved_path

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
        return manually_select_concatenation(startpath=startpath)
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
                
        cage,date = filename.split("-")[:2]
        
        # Add the full file path to the list for this key
        grouped_files[cage].append(file_path)
        
    # We only need the lists of grouped files, not the keys themselves.
    return [group for group in grouped_files.values()]

def manually_select_concatenation(startpath):
    toconcat: list[list[str]] = [select_video(title="select videos to concatenate first",path=startpath) for c in range(askint("How many concatenations?","Total Outputs"))]

    for group in toconcat:
        ready:str = concatenate(group, os.path.dirname(group[0]))
    if ready:
        clear_gpu_memory()
        os.startfile(os.path.dirname(ready))

    


# Example usage
if __name__ == "__main__":
    main()
