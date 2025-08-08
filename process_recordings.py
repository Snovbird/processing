from cagename import name_cages
from concatenate import concatenate,group_files_by_digits
from common.common import select_folder,clear_gpu_memory,find_folder_path,findval,assignval,msgbox,makefolder,error,askstring,dropdown,list_files,list_folders,list_folderspaths,list_filespaths,list_files,is_date
from markersquick import apply_png_overlay, find_imgpath_overlay_date
import os, shutil
from frameoverlay import overlay_FRAMES
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng

def process_folder():
    """Process a videos of video recordings by naming cages and concatenating videos."""
    # Select the folder to process
    initial_folder = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))
    if not initial_folder or os.path.basename(initial_folder) == "TEST_RECORDINGS":
        return
    # Check if files have already been moved
    if len(list_files(initial_folder)) == 0 and len(list_folders(initial_folder)) > 0:
        dates_dict = {os.path.basename(date_folder) : date_folder for date_folder in list_folderspaths(initial_folder) if is_date(os.path.basename(date_folder))}
        if len(dates_dict.keys()) == 0:
            error(f"Folders inside of {initial_folder} are empty")
            return
    else:
        # First, name the cages in the selected folder
        try:
            name_cages(initial_folder)
        except IndexError: # files have already been named
            pass
    # Move all videos in a folder named with date (ex:20250619)
        dates_dict = {}
        for file in [os.path.join(initial_folder, file) for file in os.listdir(initial_folder) if os.path.isfile(os.path.join(initial_folder, file))]:
            date_to_investigate = os.path.splitext(os.path.basename(file))[0].split("_")[1]
            a_date_folder = dates_dict.get(date_to_investigate, None) 
            if not a_date_folder:
                a_date_folder = makefolder(initial_folder,foldername=date_to_investigate,start_at_1=False)
                dates_dict[date_to_investigate] = a_date_folder
            shutil.move(file,a_date_folder)
    
    # variables that don't need multiple assignations
    processed_path_dir3 = find_folder_path("3-Videos ready for analysis (processed)")
    overlays_path = find_folder_path("2-MARKERS")
    room_options = list_folders(overlays_path)
    room = dropdown(room_options + ["ENTER NEW ROOM NAME"],title="Select lab test room",icon_path="dump/star.ico")
    if room == "ENTER NEW ROOM NAME":
        return emergency_overlay_maker()
    
    # Variables to store folder and image paths for each date.
    init_folderpaths = []
    ready_combined_imgs_paths = {}
    # lists of folder for different dates 
    for folder_path in list_folderspaths(initial_folder):
        files = list_files(folder_path)

        # Group files by their digit sequences for concatenation
        grouped_files = [[os.path.join(folder_path, file) for file in group] for group in group_files_by_digits(files)]
        if not grouped_files:
            print("No files found that can be grouped for concatenation.")
            return
        
        # Concatenations variables (needed for photo carrousel)
        concatenation_output_folder = makefolder(grouped_files[0][0], foldername='(delete me once done) Gradually processed videos')
        
        # Photo carroussel to verify if overlays aren't displaced
        png_outputs = makefolder(concatenation_output_folder, foldername='png')
        init_folderpaths.append(concatenation_output_folder)
        combined_output_folder = makefolder(png_outputs, foldername='combined')
        for group in grouped_files:
            bg_imgpath = extractpng(group[0],times=[1],output_folder=png_outputs)[0]
            date_for_group = os.path.splitext(os.path.basename(group[0]))[0].split("_")[1]
            cage_number = ''.join(char for char in os.path.splitext(os.path.basename(group[0]))[0][0:2] if char.isdigit()) # extract digits from first two filename characters to get cage number
            overlay_imgpath = find_imgpath_overlay_date(date_provided=date_for_group,room=room,cage_number=cage_number)
            combined_outputpath = combine_and_resize_images(bg_imgpath,overlay_imgpath,output_folder=combined_output_folder)
            ready_combined_imgs_paths[combined_outputpath] = cage_number 
    # do a carroussel of all images at once
    for imgpath, number in ready_combined_imgs_paths.items():
        if photo_carrousel(imgpath) == 'STOP markers NOT aligned':
            return emergency_overlay_maker(cage_number=number,room=room)
        
    
    # Loop through each date-named folder (usually initial_folder should only have vids for one day but this is necessary in case videos over multiple dates are present 
    for order,folder_date in enumerate(list_folders(initial_folder)):
        concatenation_output_folder = init_folderpaths[order] # get paths to folders made during photo carrousel step
        folder_path = os.path.join(initial_folder, folder_date) # folder path for each date
        files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]

        # Group files by their digit sequences for concatenation
        grouped_files = [[os.path.join(folder_path, file) for file in group] for group in group_files_by_digits(files)]
        if not grouped_files:
            error("No files found that can be grouped for concatenation.")
            return
                
        # Concatenate each group of videos
        for group in grouped_files:
            concatenate(group, concatenation_output_folder)
            clear_gpu_memory()

        # Apply Markers 
        for count, concatenated_video_path in enumerate([os.path.join(concatenation_output_folder, basename) for basename in sorted(os.listdir(concatenation_output_folder)) if os.path.isfile(os.path.join(concatenation_output_folder, basename))]):
            if count == 0:
                marked_outputs_folder = makefolder(concatenated_video_path, foldername='marked')
            if apply_png_overlay(concatenated_video_path, # if statement is to check whether the transparent overlay images exist; if DNE -> returns string "No overlay png Error"
                            marked_outputs_folder,
                            room=room,
                            cage_number=''.join(char for char in os.path.splitext(os.path.basename(concatenated_video_path))[0][0:2] if char.isdigit()),
                            ) == "Error: No overlay png":
                return emergency_overlay_maker() # STOP if can't find png
            clear_gpu_memory()

        # Overlay Frame Numbers    
        for count, marked_vid_path in enumerate([os.path.join(marked_outputs_folder, basename) for basename in sorted(os.listdir(marked_outputs_folder)) if os.path.isfile(os.path.join(marked_outputs_folder, basename))]):
            if count == 0:
                frameoverlay_output_folder = makefolder(marked_vid_path, foldername='frameoverlay-')
            if not overlay_FRAMES(marked_vid_path,
                            frameoverlay_output_folder,
                            ):
                error(f"Overlay error for:\n{marked_vid_path}\ninto {frameoverlay_output_folder}\n\nTerminating process. Please delete the folder {concatenation_output_folder}") # error if does not return output path
                return
            clear_gpu_memory()
        processed_outputfolder = makefolder(processed_path_dir3,foldername=f"{folder_date} {room.split(' ')[0]}",start_at_1=False)    
        msgbox(processed_outputfolder)
        for file in [os.path.join(frameoverlay_output_folder, basename) for basename in sorted(os.listdir(frameoverlay_output_folder)) if os.path.isfile(os.path.join(frameoverlay_output_folder, basename))]:
            final_output_path = shutil.move(file,processed_outputfolder)
        import time
        while True:
            try:
                shutil.rmtree(concatenation_output_folder)
                break
            except Exception as e:
                print(f"Error deleting folder {concatenation_output_folder}: {e}")
                time.sleep(1)
    msgbox(msg="Video Processing complete!",title="Success")

    os.startfile(processed_outputfolder)

    dates_count = len(list_folders(initial_folder))
    if dates_count> 1:
        os.startfile(processed_path_dir3)
    elif dates_count == 1:
        os.startfile(os.path.dirname(final_output_path)) # folder specific


def emergency_overlay_maker(cage_number=None,room=None):
    from common.common import get_date_yyyymmdd,select_video,askint
    marker_overlays_path = find_folder_path("2-MARKERS")
    date = askstring("Please enter the date as YYYYMMDD for this overlay. \nDefault is today's date.",fill=get_date_yyyymmdd())
    room_folder_path = os.path.join(marker_overlays_path,room)
    if not cage_number:
        cage_number = askint("Enter the cage number:","Cage number")
        if not cage_number:
            return
    
    if not room:
        room = askstring("Provide the name of the new room:","New room name",fill="ROOMNAME (numberofcages)")
        room_folder_path = makefolder(marker_overlays_path,foldername=room,start_at_1=False)
    else:
        # ↓ alternative name needed | working path
        room_folder_path = makefolder(room_folder_path,f"cage{cage_number}_{date}.psd",start_at_1=False)
    
    first_psdfile_path = shutil.copy(os.path.join(find_folder_path("PSD_TEMPLATES_MARKERS"),"templatepsd.psd"),room_folder_path)
    # name example = cage6_20250616.png
    psdfile_path = os.path.join(room_folder_path,f"cage{cage_number}_{date}.psd")
    os.rename(first_psdfile_path,psdfile_path)
    os.startfile(room_folder_path)
    msgbox("A folder will open next. From the explorer, select a video from which an image will be extracted align the markers.\nThis image will be automatically added to the opened folder.")
    times = 1
    imgpath = extractpng(video=select_video("Select video from which an image will be extracted align the markers"),times=(times,),output_folder=room_folder_path)[0]
    while photo_carrousel(imgpath,"OK. All cue lights are lit.","NO. Jump 5s to find all 4 cue lights ON") !="OK. All cue lights are lit.":
        os.remove(imgpath)
        times += 5
        imgpath = extractpng(video=select_video("Select video from which an image will be extracted align the markers"),times=(times,),output_folder=room_folder_path)[0]
    os.startfile(room_folder_path)


if __name__ == "__main__":
    # process_folder()
    process_folder()