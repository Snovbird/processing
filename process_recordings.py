from cagename import name_cages
from concatenate import combine_videos_with_cuda,group_files_by_digits
from common.common import select_video,clear_gpu_memory,get_date_mmdd,find_folder_path,findval,assignval
from markersquick import apply_png_overlay
import os
import shutil
def process_folder():
    """Process a videos of video recordings by naming cages and concatenating videos."""
    # Select the videos to process
    folder_path = select_video("Select ALL videos to process")
    if not folder_path:
        return
    
    # First, name the cages in the selected videos
    name_cages(folder_path)
    
    # Get all video files in the videos
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    # Group files by their digit sequences for concatenation
    grouped_files = group_files_by_digits(files)
    
    if not grouped_files:
        print("No files found that can be grouped for concatenation.")
        return
        
    # Convert relative paths to absolute paths
    grouped_files = [[os.path.join(folder_path, file) for file in group] for group in grouped_files]
    
    # Create output videos for concatenated videos
    from common.common import makefolder
    concatenation_output_folder = makefolder(grouped_files[0][0], foldername='concat')
    
    # Concatenate each group of videos
    for group in grouped_files:
        combine_videos_with_cuda(group, concatenation_output_folder)
        if clear_gpu_memory():
            pass
    did_break = None
    for count, concatenated_video_path in enumerate([os.path.join(concatenation_output_folder, basename) for basename in sorted(os.listdir(concatenation_output_folder)) if os.path.isfile(os.path.join(concatenation_output_folder, basename))]):
        if count == 0:
            marked_outputs_folder = makefolder(concatenated_video_path, foldername='marked')
        if apply_png_overlay(concatenated_video_path,
                          marked_outputs_folder,
                          cage_number=''.join(char for char in os.path.splitext(os.path.basename(concatenated_video_path))[0][0:2] if char.isdigit()),
                          thedate=get_date_mmdd(),
                          overlays_path=find_folder_path("2-MARKERS")
                          ) == "No Overlay Error":
            did_break = True
            break
        if clear_gpu_memory():
            pass
    else:
        os.startfile(marked_outputs_folder)
    if did_break:
        emergency_overlay_maker()

def emergency_overlay_maker():
    shutil.copy()
if __name__ == "__main__":
    process_folder()
