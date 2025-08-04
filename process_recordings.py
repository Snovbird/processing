from cagename import name_cages
from concatenate import combine_videos_with_cuda,group_files_by_digits
from common.common import select_folder,clear_gpu_memory,find_folder_path,findval,assignval,makefolder,error,get_date_yyyymmdd,askstring
from markersquick import apply_png_overlay
import os, shutil
from frameoverlay import overlay_FRAMES
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images

def process_folder():
    """Process a videos of video recordings by naming cages and concatenating videos."""
    # Select the folder to process
    folder_path = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))
    if not folder_path:
        return
    
    # First, name the cages in the selected folder
    name_cages(folder_path)
    
    # Get all video files in the folder
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    # Group files by their digit sequences for concatenation
    grouped_files = group_files_by_digits(files)
    
    if not grouped_files:
        print("No files found that can be grouped for concatenation.")
        return
        
    # Convert relative paths to absolute paths
    grouped_files = [[os.path.join(folder_path, file) for file in group] for group in grouped_files]
    
    # Create output videos for concatenated videos
    concatenation_output_folder = makefolder(grouped_files[0][0], foldername='(not ready) processed videos')

    # ask and initiate variables to find what markers to use
    overlays_path = find_folder_path("2-MARKERS")
    room_options = os.listdir(overlays_path)
    stroption = '\n'.join(room_options)
    room = askstring(msg=f"Enter the name of the room. Options are:\n{stroption}")
    date_today = get_date_yyyymmdd()
    alldates = findval("dates")[::-1] # invert it to loop from latest dates first then to earlier ones
    ready_combined_imgs_paths = []

    combined_output_folder = makefolder(concatenation_output_folder, foldername='combined')
    for group in grouped_files:
        cage_number = ''.join(char for char in os.path.splitext(os.path.basename(group[0]))[0][0:2] if char.isdigit()) # extract digits from first two filename characters to get cage number
        for d in range(alldates.index(date_today),len(alldates)):
            imagepath = os.path.join(overlays_path, room,f"cage{cage_number}{alldates[d]}.png") # f"{width}/cage{cage_number}_{alldates[d]}_{width}.png")
            if os.path.exists(imagepath):
                break
        else:
            error(msg=f"There is no overlay images for cage {cage_number}.\nPath '{imagepath}' does not exist")
        combined_outputpath = combine_and_resize_images(group[0],imagepath,output_folder=combined_output_folder)
        ready_combined_imgs_paths.append(combined_outputpath)
    
    for img in ready_combined_imgs_paths:
        if photo_carrousel(img) == 'STOP markers NOT aligned':
            return emergency_overlay_maker()


    # Concatenate each group of videos
    for group in grouped_files:
        combine_videos_with_cuda(group, concatenation_output_folder)
        if clear_gpu_memory():
            pass
    did_break = None

    for count, concatenated_video_path in enumerate([os.path.join(concatenation_output_folder, basename) for basename in sorted(os.listdir(concatenation_output_folder)) if os.path.isfile(os.path.join(concatenation_output_folder, basename))]):
        if count == 0:
            marked_outputs_folder = makefolder(concatenated_video_path, foldername='marked')
        if apply_png_overlay(concatenated_video_path, # if statement is to check whether the transparent overlay images exist; if DNE -> returns string "No overlay png Error"
                          marked_outputs_folder,
                          cage_number=''.join(char for char in os.path.splitext(os.path.basename(concatenated_video_path))[0][0:2] if char.isdigit()),
                          thedate=get_date_yyyymmdd(),
                          overlays_path=find_folder_path("2-MARKERS")
                          ) == "Error: No overlay png":
            os.remove(concatenation_output_folder)
            return emergency_overlay_maker()
            
        if clear_gpu_memory():
            pass
    else:
        for count, marked_vid_path in enumerate([os.path.join(marked_outputs_folder, basename) for basename in sorted(os.listdir(marked_outputs_folder)) if os.path.isfile(os.path.join(marked_outputs_folder, basename))]):
            if count == 0:
                frameoverlay_output_folder = makefolder(marked_vid_path, foldername='frameoverlay-')
            if not overlay_FRAMES(marked_vid_path,
                            frameoverlay_output_folder,
                            ):
                error(f"Overlay error for:\n{marked_vid_path}\ninto {frameoverlay_output_folder}") # error if does not return output path
            
            if clear_gpu_memory():
                pass
        final_output_folder = makefolder(folder_path,foldername="VIDEOS READY FOR ANALYSIS-")    
        for file in [os.path.join(frameoverlay_output_folder, basename) for basename in sorted(os.listdir(frameoverlay_output_folder)) if os.path.isfile(os.path.join(frameoverlay_output_folder, basename))]:
            shutil.move(file,final_output_folder)
        
        os.remove(concatenation_output_folder)

def emergency_overlay_maker():
    # shutil.copy(photoshop project)
    pass



if __name__ == "__main__":
    # process_folder()
    process_folder()