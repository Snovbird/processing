import subprocess
import tempfile
import os
from common.common import select_video,askint,windowpath,clear_gpu_memory,makefolder

def combine_videos_with_cuda(input_files, output_folder):
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
