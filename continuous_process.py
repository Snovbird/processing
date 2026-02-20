from common.common import *
import os, shutil,time
from cagename import name_cages
from concatenate import concatenate, group_files_by_digits
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng
from markersquick import apply_png_overlay,find_imgpath_overlay_date
from newtrim import trim_DS_auto
from process_folders import group_by_date_and_experimentTime, emergency_overlay_maker

def reset_saved():
    assignval("salvage_processing_step", {})

def step1_organize_recordings_DATASAVE():
    last_step = findval("salvage_processing_step")
    if last_step and "step1_organize_recordings_DATASAVE" not in last_step:
        return step2_create_folders_and_move()

    recording_folderpath = last_step["step1_organize_recordings_DATASAVE"]["recordings_folder"]
    grouped_recordings = last_step["step1_organize_recordings_DATASAVE"]["grouped_recordings"]
    {'20251103': [['01-20251103-104708-113000.mp4', '01-20251103-113000-114505.mp4','03-20251103-104708-113000.mp4'], #exp1
                  ['01-20251103-122945-130000.mp4', '01-20251103-130000-133000.mp4']], #experiment 2
    '20251104': [['01-20251104-093838-100000.mp4', '01-20251104-100000-103000.mp4'], 
                 ['01-20251104-112135-120000.mp4', '01-20251104-120000-122642.mp4']]}

    override_first_cue = findval("salvage_processing_step")["step1_organize_recordings_DATASAVE"]["override_first_cue"]

    folders_to_create = []
    for date_number, (date,experiment_groups) in enumerate(grouped_recordings.items()): # unpack dates
        
        date_folderpath = makefolderpath(os.path.dirname(recording_folderpath), foldername=date, start_at_1=False)

        folders_to_create.append({"date_folderpath": date_folderpath,"experiment_folders":[],"grouped_experiments":[]})
        
        grid_rownames = []
        for experiment_number,videos_per_experiment in enumerate(experiment_groups,start=1): #make question string
            first = videos_per_experiment[0]
            time_start = first.split("-")[2]
            hour = time_start[0:2]
            minute = time_start[2:4]
            row_name_question = f"Experiment #{experiment_number} at {hour}:{minute}"
            grid_rownames.append(row_name_question)
            
        if override_first_cue:
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each experiment (row names)
                                                    options_list=["DS+","DS-","SEEKING_TEST"], # options for each row
                                    title="First Cue",
                                    message=f"Select the first cue illuminated in experiments on {date}"
                                    )
            answer = list(answer_dict.values())
        else: 
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each experiment (row names)
                                                    options_list=["YES","NO"], # options for each row
                                    title="Merge wrongly separated experiments",
                                    message=f"Are these separate experiments on {date}"
                                    )
            answer = list(answer_dict.values())

            for i, ans in enumerate(answer):
                if ans == "NO":
                    experiment_groups[i-1].extend(experiment_groups[i])
                    experiment_groups[i-1].sort()
                    del experiment_groups[i]

            answer = ["SEEKING_TEST"] * len(experiment_groups)

        for experiment_number, first_DS in enumerate(answer, start=0): 
            # first_DS is either DS+, DS- or SEEKING_TEST

            folder_name = makefolderpath(date_folderpath,f"{date}_{experiment_number} {first_DS}", start_at_1=False)

            folders_to_create[date_number]["experiment_folders"].append(folder_name)
            folders_to_create[date_number]["grouped_experiments"].append((experiment_groups[experiment_number]))

        print(f"{folders_to_create=}")

        assignval("salvage_processing_step", {"step2_create_folders_and_move":{
            "recordings_folderpath": recording_folderpath,
            "folders_to_create": folders_to_create}})
        
        step2_create_folders_and_move()

def step2_create_folders_and_move():

    last_step = findval("salvage_processing_step")
    if "step2_create_folders_and_move" not in last_step:
        return step3_create_photos_for_carroussel()

    recording_folderpath = last_step["step2_create_folders_and_move"]["recordings_folderpath"]
    folders_to_create = last_step["step2_create_folders_and_move"]["folders_to_create"]
    [{
        "date_folderpath": "D:\\0-RECORDINGS\\20251103",
        "experiment_folders": [
            "D:\\0-RECORDINGS\\20251103_0 SEEKING_TEST",
            "D:\\0-RECORDINGS\\20251103_1 SEEKING_TEST"
        ],
        "grouped_experiments": [
            [
                "01-20251103-104708-113000.mp4",
                "01-20251103-113000-114505.mp4",
                "01-20251103-114505-115321.mp4"
            ],
            [
                "01-20251103-122945-130000.mp4",
                "01-20251103-130000-133000.mp4",
                "01-20251103-133000-133154.mp4"
            ]
        ]
    },
    {
        "date_folderpath": "D:\\0-RECORDINGS\\20251104",
        "experiment_folders": [
            "D:\\0-RECORDINGS\\20251104_0 SEEKING_TEST",
            "D:\\0-RECORDINGS\\20251104_1 SEEKING_TEST"
        ],
        "grouped_experiments": [
            [
                "01-20251104-093838-100000.mp4",
                "01-20251104-100000-103000.mp4",
                "01-20251104-103000-104158.mp4"
            ],
            [
                "01-20251104-112135-120000.mp4",
                "01-20251104-120000-122642.mp4"
            ]]}]
    
    last_step["moved"] = last_step.get("moved",[])

    for date_info in folders_to_create:
        date_folderpath = date_info["date_folderpath"]
        experiment_folders = date_info["experiment_folders"]
        grouped_experiments = date_info["grouped_experiments"]

        os.makedirs(date_folderpath, exist_ok=True)
        for experiment_folder in experiment_folders:
            os.makedirs(experiment_folder, exist_ok=True)

        for experiment_folder, experiment_videos in zip(experiment_folders, grouped_experiments):
            
            for video in experiment_videos:
                if video in last_step["moved"]:
                    continue
                video_path = os.path.join(recording_folderpath, video)
                dst = experiment_folder
                shutil.move(video_path, dst)
                
                last_step["moved"].append(video)

                assignval("salvage_processing_step", last_step)
    else:
        time.sleep(1)
        os.rmdir(recording_folderpath)

        assignval("salvage_processing_step", {"step3_create_photos_for_carroussel":{
        "experiment_folders": experiment_folders,}})

def step3_create_photos_for_carroussel():
    last_step = findval("salvage_processing_step")
    if "step3_create_photos_for_carroussel" not in last_step:
        return step4_created_combined_and_photo_carrousel()
    
    experiment_folders = last_step["step3_create_photos_for_carroussel"]["experiment_folders"]
    
    experiment_and_png_folders = {}
    photos_to_add_ = []
    
    for experiment_folder in experiment_folders:
        experiment_and_png_folders[experiment_folder] = makefolder(experiment_folder, "photos", start_at_1=False)

    for experiment_folder, photos_folder in experiment_and_png_folders.items():
        # Get videos in experiment folder
        videos = list_filespaths(experiment_folder)
        # Group by cage (digits) to get the first video of each cage
        for cage_group in group_files_by_digits(videos):
            first_video = cage_group[0]
            
            # Extract screenshot from the FIRST frame (frame_number=0)
            # This screenshot will be used to verify markers
            # common.common.screenshot
            photos_to_add_.append(
                screenshot(first_video, frame_number=0,
                            output_path=os.path.join(photos_folder, 
                                                    os.path.basename(first_video).replace(".mp4", ".png"))
                            )
            )

    # Save state for the next step (step 4)
    assignval("salvage_processing_step", {
        "step4_created_combined_and_photo_carrousel": {
            "experiment_and_png_folders": experiment_and_png_folders, # experiment_folder : photos folder
            "photos_to_add_": photos_to_add_
        }
    })
    # {'experiment_folders': ['D:\\0-RECORDINGS\\20251103_1 SEEKING_TEST', ...],
    #  'experiment_and_png_folders': {'D:\\0-RECORDINGS\\20251103_1 SEEKING_TEST': 'D:\\0-RECORDINGS\\20251103_1 SEEKING_TEST\\photos', ...},
    #  'photos_to_add_': ['D:\\0-RECORDINGS\\20251103_1 SEEKING_TEST\\photos\\01-20251103-104708-113000.png', ...]}
    
    return step4_created_combined_and_photo_carrousel()

def step4_created_combined_and_photo_carrousel():
    last_step = findval("salvage_processing_step")
    if "step4_created_combined_and_photo_carrousel" not in last_step:
        # Logic to skip if we are already past this step
        return step5_concatenate_videos()

    experiment_folders:list[str] = list(last_step["step4_created_combined_and_photo_carrousel"]["experiment_and_png_folders"].keys())
    experiment_and_png_folders:dict[str,str] = list(last_step["step4_created_combined_and_photo_carrousel"]["experiment_and_png_folders"].values())
    photos_to_add_:list[str] = last_step["step4_created_combined_and_photo_carrousel"]["photos_to_add_"]

    created_photos:list[str] = last_step["step4_created_combined_and_photo_carrousel"].get("created_photos", []) 
    last_step["step4_created_combined_and_photo_carrousel"]["created_photos"] = created_photos # Initialize if not present
    room_options = list_folders(find_folder_path("2-MARKERS"))
    
    # Try to find room in data.json or ask user
    saved_room = findval("room_name")
    if saved_room and saved_room in room_options:
        room = saved_room
    else:
        room = dropdown(room_options + ["ENTER NEW ROOM NAME"], title="Select lab test room", icon_name="star", hide=("MARKERS-TEMPLATES",))
        if room == "ENTER NEW ROOM NAME":
            return emergency_overlay_maker()
        assignval("room_name", room)

    for photopath in photos_to_add_:

        basename = os.path.splitext(os.path.basename(photopath))[0]
        combpath = os.path.join(os.path.dirname(photopath), f"{basename}_combined.png")
        if combpath in created_photos:
            continue
        # naming convention: cage-date-time-time
        # e.g. 01-20251103-104708-113000
        parts = basename.split("-")
        cage_string = parts[0]
        date = parts[1]
        cage_number = "".join([i for i in cage_string if i.isdigit()])
        
        overlay = find_imgpath_overlay_date(date, room=room, cage_number=cage_number)
        
        outpath = os.path.dirname(photopath)
        
        # image_combine.combine_and_resize_images
        created_combined_paths = combine_and_resize_images(photo1_path=photopath,
                                                             photo2_path=overlay,
                                                             output_folder=outpath)
        if created_combined_paths == combpath:
            created_photos.append(created_combined_paths)

    for overlaid_png in created_photos:
        result = photo_carrousel(overlaid_png) 
        if result == "STOP markers NOT aligned":
            basename = os.path.splitext(os.path.basename(overlaid_png))[0].replace("_combined","")
            cage_string, date, *_ = basename.split("-")
            cage_number = "".join([i for i in cage_string if i.isdigit()])
            parent_combinedpng_folder = os.path.dirname(overlaid_png) 
            # The photo is in .../Experiment/photos/
            # The video is in .../Experiment/
            experiment_dir = os.path.dirname(parent_combinedpng_folder)

            created_photos.remove(overlaid_png)
            assignval("salvage_processing_step",last_step) # remove problematic image
            
            problematic_videopath = None
            for video in list_filespaths(experiment_dir):
                vid_basename = os.path.splitext(os.path.basename(video))[0]
                if vid_basename == basename:
                    problematic_videopath = video
                    break
            
            if not problematic_videopath:
                error(f"No matching video file found for {basename} in {experiment_dir}")
                return

            return emergency_overlay_maker(cage_numbers=[cage_number], room=room, date=date, videos=[problematic_videopath])

    # Cleanup photos folders
    for folder in experiment_and_png_folders.values():
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print(f"Error removing {folder}: {e}")

    # Save state for step 5
    assignval("salvage_processing_step", {
        "step5_concatenate_videos": {
            "experiment_folders": experiment_folders,
            "room": room
        }
    })
    # {'experiment_folders': [...], 'room': 'Room 1'}

    return step5_concatenate_videos()

def step5_concatenate_videos():
    last_step = findval("salvage_processing_step")
    if "step5_concatenate_videos" not in last_step:
         return step6_trim_intervals()

    experiment_folders = last_step["step5_concatenate_videos"]["experiment_folders"]
    room = last_step["step5_concatenate_videos"]["room"]
    
    videos_to_delete:list[list[str]] = last_step["step5_concatenate_videos"].get("videos_to_delete", []) # Load if partly done
    last_step["step5_concatenate_videos"]["videos_to_delete"] = videos_to_delete    
    processed_folders = last_step["step5_concatenate_videos"].get("processed_folders", [])
    last_step["step5_concatenate_videos"]["processed_folders"] = processed_folders    

    for experiment_folder in experiment_folders:
        if experiment_folder in processed_folders:
            continue

        videos = list_filespaths(experiment_folder)
        if len(videos) == 0:
            continue
        
        grouped_videos = group_files_by_digits(videos) # important to update (if 2nd time) due to renaming if len(group) == 1
        
        for group in grouped_videos:

            if not group or group in videos_to_delete:
                continue
            if len(group) == 1:
                saved_path = concatenate(group, experiment_folder) 
                videos_to_delete.append((saved_path,)) # tuple for len == 1 check (will not be deleted). Same list for simplicity (check of group in videos_to_delete)
            else:
                concatenate(group, experiment_folder) 
                videos_to_delete.append(group) 
            assignval("salvage_processing_step", last_step)

        processed_folders.append(experiment_folder)
        assignval("salvage_processing_step", last_step)

    for vid_group in videos_to_delete:
        if not vid_group or len(vid_group) == 1: # has been renamed by concatenate(). DO NOT DELETE
            continue
        for vid in vid_group:
            try:
                if os.path.exists(vid):
                    os.remove(vid)
                    print(f"Deleted original video: {os.path.basename(vid)}")
            except Exception as e:
                error(f"Error deleting {vid}\n\nError: {e}")
    
    assignval("salvage_processing_step", {
        "step6_trim_intervals": {
            "experiment_folders": experiment_folders,
            "room": room
        }
    })

    return step6_trim_intervals()

def step6_trim_intervals():
    last_step = findval("salvage_processing_step")
    if "step6_trim_intervals" not in last_step:
        return step7_apply_markers_and_move()

    experiment_folders = last_step["step6_trim_intervals"]["experiment_folders"]
    room = last_step["step6_trim_intervals"]["room"]
    
    trimmed_folders = last_step["step6_trim_intervals"].get("trimmed_folders", [])
    last_step["step6_trim_intervals"]["trimmed_folders"] = trimmed_folders

    for experiment_folder in experiment_folders:
        if experiment_folder in trimmed_folders:
            continue
            
        # e.g. "D:\\...\\20251103_1 SEEKING_TEST"
        # The prompt says: DS_cue = experiment.split(" ")[-1]
        DS_cue = experiment_folder.split(" ")[-1]
        if DS_cue not in ["DS+","DS-"]:
            continue # Skip trimming if not DS+ or DS- (e.g. SEEKING_TEST)

        videos = list_filespaths(experiment_folder)
        try:
            trim_DS_auto(videos, first=DS_cue, start_time=16, interval_duration=90, batch_size=5) # no need to save progress for each of DS+, DS- & CS+
        except Exception as e:
            error(f"Error trimming {experiment_folder}: {e}")
            
        trimmed_folders.append(experiment_folder)
        assignval("salvage_processing_step", last_step)

    assignval("salvage_processing_step", {
        "step7_apply_markers_and_move": {
            "experiment_folders": experiment_folders,
            "room": room
        }
    })
    
    return step7_apply_markers_and_move()

def step7_apply_markers_and_move():
    last_step = findval("salvage_processing_step")
    if "step7_apply_markers_and_move" not in last_step:
        # Done?
        error("Error finding last saved step. Starting over.")
        assignval("salvage_processing_step", {}) # Clear state
        continuous_process()
        return

    experiment_folders = last_step["step7_apply_markers_and_move"]["experiment_folders"]
    room = last_step["step7_apply_markers_and_move"]["room"]
    created_marked_videos = last_step["step7_apply_markers_and_move"].get("created_marked_videos", [])
    last_step["step7_apply_markers_and_move"]["created_marked_videos"] = created_marked_videos
    created_marker_folders = last_step["step7_apply_markers_and_move"].get("created_marker_folders", [])
    last_step["step7_apply_markers_and_move"]["created_marker_folders"] = created_marker_folders

    # final_outputpath = find_folder_path("3-PROCESSED")
    final_outputpath = r"D:\0-RECORDINGS\test_output"
    

    for experiment_folder in experiment_folders:
        basename = os.path.basename(experiment_folder)
        # Create folder for marked videos inside the experiment folder (temp)
        if experiment_folder not in created_marker_folders:
            marked_folder = makefolder(experiment_folder, basename, start_at_1=False)
            created_marker_folders.append(experiment_folder)
            assignval("salvage_processing_step", last_step)
        # Apply overlay to all videos in the experiment folder
        # The videos here are presumably the concatenated (and possibly trimmed output?)
        # process_folders logic: for concat_vid in list_filespaths(experiment)
        
        for vid in list_filespaths(experiment_folder):
             # markersquick.apply_png_overlay
             if vid in created_marked_videos:
                 continue
             
             apply_png_overlay(vid, marked_folder, room)
             created_marked_videos.append(vid)
             assignval("salvage_processing_step", last_step)

    # Move content to final output
    for folder in created_marker_folders:
        try:
            shutil.move(folder, final_outputpath)
        except Exception as e:
            error(f"Error moving {folder} to {final_outputpath}: {e}")
            
    msgbox(f"Video processing complete!\n\nPrepared videos are stored in {final_outputpath}.\nClose this message to open the folder.")
    assignval("salvage_processing_step", {})
    os.startfile(final_outputpath) # Open final output folder


def continuous_process(recordings_folder=None):

    if not findval("salvage_processing_step"):
        if not recordings_folder:
            recordings_folder = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))

        assignval("room_name", "OPTO-ROOM (12 cages)")
        try:
            name_cages(recordings_folder)
        except Exception as e:
            print("Cages already renamed")
            pass

        override_first_cue = True if custom_dialog("Separate each video into DS+/DS- intervals (for training only)?", title="Specify first cue for each experiment?") == "yes" else False
        
        grouped_recordings = group_by_date_and_experimentTime(recordings_folder,max_pause=750,warn_for_lost_time=True)

        assignval("salvage_processing_step", {"step1_organize_recordings_DATASAVE": 
                                              {"recordings_folder": recordings_folder, 
                                               "grouped_recordings": grouped_recordings,
                                               "override_first_cue": override_first_cue}})
        step1_organize_recordings_DATASAVE()
    else:
        last_command = list(findval("salvage_processing_step").keys())[0]
        exec(f"{last_command}()")

if __name__ == "__main__":
    continuous_process()