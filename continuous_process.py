from common.common import *
import os, shutil,time
from cagename import name_cages
from concatenate import concatenate, group_files_by_digits
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng
from markersquick import apply_png_overlay,find_overlay_path
from newtrim import trim_DS_auto
from process_folders import group_by_date_and_sessionTime, emergency_overlay_maker
    

def reset_saved():
    assignval("salvage_processing_step", {})

def step1_organize_recordings_DATASAVE():
    """
    create appropriate folders for each date and sessions for this date
    """
    last_step = findval("salvage_processing_step")
    if last_step and "step1_organize_recordings_DATASAVE" not in last_step:
        return step2_create_folders_and_move()

    recording_folderpath = last_step["step1_organize_recordings_DATASAVE"]["recordings_folder"]
    grouped_recordings = last_step["step1_organize_recordings_DATASAVE"]["grouped_recordings"]

    override_first_cue = findval("salvage_processing_step")["step1_organize_recordings_DATASAVE"]["override_first_cue"]

    folders_to_create = []
    for date_number, (date,session_groups) in enumerate(grouped_recordings.items()): # unpack dates
        
        date_folderpath = makefolder(os.path.dirname(recording_folderpath), foldername=date, start_at_1=False)

        folders_to_create.append({"date_folderpath": date_folderpath,"session_folders":[],"grouped_sessions":[]})
        
        grid_rownames = []
        for session_number,videos_per_session in enumerate(session_groups,start=1): #make question string
            first = videos_per_session[0]
            time_start = first.split("-")[2]
            hour = time_start[0:2]
            minute = time_start[2:4]
            row_name_question = f"Experiment #{session_number} at {hour}:{minute}"
            grid_rownames.append(row_name_question)
            
        if override_first_cue:
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each session (row names)
                                                    options_list=["DS+","DS-","session"], # options for each row
                                    title="First Cue",
                                    message=f"Select the first cue illuminated in sessions on {date}"
                                    )
            answer = answer_dict

            for session_number, qna in enumerate(answer, start=0): 
                question, first_DS = qna.items()

                time = question[0].split(" at ")[-1].replace(":","")
                # first_DS is either DS+, DS- or session
                folder_name = makefolder(date_folderpath,f"{date} at {time} {first_DS}", start_at_1=False)
                folders_to_create[date_number]["session_folders"].append(folder_name)
                folders_to_create[date_number]["grouped_sessions"].append((session_groups[session_number]))

        else: 
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each session (row names)
                                                    options_list=["YES","NO"], # options for each row
                                    title="Merge wrongly separated sessions",
                                    message=f"Are these separate sessions on {date}"
                                    )
            answer = list(answer_dict.values())

            merged_sessions = []
            for i, ans in enumerate(answer):
                if ans == "NO":
                    merged_sessions[i-1].extend(session_groups[i])
                    session_groups[i-1].sort()
                else:
                    merged_sessions.append(session_groups[i])

            for session_number,merged_sess in enumerate(merged_sessions): 
                folder_name = makefolder(date_folderpath,f"{date}_{session_number+1} session", start_at_1=False)
                folders_to_create[date_number]["session_folders"].append(folder_name)
                folders_to_create[date_number]["grouped_sessions"].append((merged_sess))

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
    last_step["moved"] = last_step.get("moved",[])
    all_session_folders = []

    for date_info in folders_to_create:
        date_folderpath = date_info["date_folderpath"]
        session_folders = date_info["session_folders"]
        grouped_sessions = date_info["grouped_sessions"]
        
        all_session_folders.extend(session_folders)

        for session_folder, session_videos in zip(session_folders, grouped_sessions):
            
            for video in session_videos:
                if video in last_step["moved"]:
                    continue
                video_path = os.path.join(recording_folderpath, video)
                dst = session_folder
                try:
                    shutil.move(video_path, dst)
                except Exception as e:
                    print(f"Error occurred while moving {video}: {e}")
                    continue

                last_step["moved"].append(video)

                assignval("salvage_processing_step", last_step)
    else:
        time.sleep(1)
        if len(list_files_ext(recording_folderpath,ext=".mp4")) == 0:
            walk_delete(recording_folderpath)

        assignval("salvage_processing_step", {"step3_create_photos_for_carroussel":{
        "session_folders": all_session_folders}})

        step3_create_photos_for_carroussel()

def step3_create_photos_for_carroussel():
    last_step = findval("salvage_processing_step")
    if "step3_create_photos_for_carroussel" not in last_step:
        return step4_created_combined_and_photo_carrousel()
    
    session_folders = last_step["step3_create_photos_for_carroussel"]["session_folders"]
    
    session_and_png_folders = {}
    photos_to_add_ = []
    
    for session_folder in session_folders:
        session_and_png_folders[session_folder] = makefolder(session_folder, "photos", start_at_1=False)

    for session_folder, photos_folder in session_and_png_folders.items():
        # Get videos in session folder
        videos = list_filespaths(session_folder)
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
            "session_and_png_folders": session_and_png_folders, # session_folder : photos folder
            "photos_to_add_": photos_to_add_
        }
    })
    # {'session_folders': ['D:\\0-RECORDINGS\\20251103_1 session', ...],
    #  'session_and_png_folders': {'D:\\0-RECORDINGS\\20251103_1 session': 'D:\\0-RECORDINGS\\20251103_1 session\\photos', ...},
    #  'photos_to_add_': ['D:\\0-RECORDINGS\\20251103_1 session\\photos\\01-20251103-104708-113000.png', ...]}
    
    return step4_created_combined_and_photo_carrousel()

def step4_created_combined_and_photo_carrousel():
    last_step = findval("salvage_processing_step")
    if "step4_created_combined_and_photo_carrousel" not in last_step:
        # Logic to skip if we are already past this step
        return step5_concatenate_videos()

    session_folders:list[str] = list(last_step["step4_created_combined_and_photo_carrousel"]["session_and_png_folders"].keys())
    png_folders:list[str] = list(last_step["step4_created_combined_and_photo_carrousel"]["session_and_png_folders"].values())
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
            newroom = askstring("Enter new room name", "New Room Name")

            return emergency_overlay_maker(room=newroom)
        assignval("room_name", room)

    for photopath in photos_to_add_:

        basename = os.path.splitext(os.path.basename(photopath))[0]
        combpath = os.path.join(os.path.dirname(photopath), f"{basename}_combined.png") # not supposed to exist yet if this is the first time
        if combpath in created_photos:
            continue
        # naming convention: cage-date-time-time
        # e.g. 01-20251103-104708-113000
        try:
            overlay = find_overlay_path(photopath, room=room)
        except ImageNotFoundError as e:      
            print(e)
            emergency_overlay_maker(photopath, room=room)
        
        # image_combine.combine_and_resize_images
        created_combined_path = combine_and_resize_images(photo1_path=photopath,
                                                             photo2_path=overlay)
        if created_combined_path == combpath:
            created_photos.append(created_combined_path)
    created_photos.sort(key= lambda x: os.path.basename(x).split("-")[1] + os.path.basename(x).split("-")[2])
    for overlaid_png in created_photos:
        result = photo_carrousel(overlaid_png) 
        if result == "STOP markers NOT aligned":
            basename = os.path.splitext(os.path.basename(overlaid_png))[0].replace("_combined","")
            cage_string, date, *_ = basename.split("-")
            cage_number = "".join([i for i in cage_string if i.isdigit()])
            parent_combinedpng_folder = os.path.dirname(overlaid_png) 
            # The photo is in .../Experiment/photos/
            # The video is in .../Experiment/
            session_dir = os.path.dirname(parent_combinedpng_folder)
            
            created_photos.remove(overlaid_png) # note: re-created images will be put at the end of the carroussel, but still be present (only order will be different)
            assignval("salvage_processing_step",last_step) # remove problematic image
            
            problematic_videopath = None
            for video in list_filespaths(session_dir):
                vid_basename = os.path.splitext(os.path.basename(video))[0]
                if vid_basename in basename or basename in vid_basename:
                    problematic_videopath = video
                    break
            
            if not problematic_videopath:
                raise Exception(f"No matching video file found for {basename} in {session_dir}")

            return emergency_overlay_maker(problematic_videopath,room=room)

    # Cleanup photos folders
    for folder in png_folders:
        try:
            shutil.rmtree(folder)
        except OSError as e:
            print(f"Error removing {folder}: {e}")

    # Save state for step 5
    assignval("salvage_processing_step", {
        "step5_concatenate_videos": {
            "session_folders": session_folders,
            "room": room
        }
    })
    # {'session_folders': [...], 'room': 'Room 1'}

    return step5_concatenate_videos()

def step5_concatenate_videos():
    last_step = findval("salvage_processing_step")
    if "step5_concatenate_videos" not in last_step:
         return step6_trim_intervals()

    session_folders = last_step["step5_concatenate_videos"]["session_folders"]
    room = last_step["step5_concatenate_videos"]["room"]
    
    videos_to_delete:list[list[str]] = last_step["step5_concatenate_videos"].get("videos_to_delete", []) # Load if partly done
    last_step["step5_concatenate_videos"]["videos_to_delete"] = videos_to_delete    
    processed_folders = last_step["step5_concatenate_videos"].get("processed_folders", [])
    last_step["step5_concatenate_videos"]["processed_folders"] = processed_folders    

    for session_folder in session_folders:
        if session_folder in processed_folders:
            continue

        videos = list_filespaths(session_folder)
        if len(videos) == 0:
            continue
        
        grouped_videos = group_files_by_digits(videos) # important to update (if 2nd time) due to renaming if len(group) == 1
        
        for group in grouped_videos:

            if not group or group in videos_to_delete:
                continue
            if len(group) == 1:
                saved_path = concatenate(group, session_folder) 
                videos_to_delete.append((saved_path,)) # tuple for len == 1 check (will not be deleted). Same list for simplicity (check of group in videos_to_delete)
            else:
                concatenate(group, session_folder) 
                videos_to_delete.append(group) 
            assignval("salvage_processing_step", last_step)

        processed_folders.append(session_folder)
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
            "session_folders": session_folders,
            "room": room
        }
    })

    return step6_trim_intervals()

def step6_trim_intervals(): # currently unusable
    last_step = findval("salvage_processing_step")
    if "step6_trim_intervals" not in last_step:
        return step7_apply_markers_and_move()

    session_folders = last_step["step6_trim_intervals"]["session_folders"]
    room = last_step["step6_trim_intervals"]["room"]
    
    trimmed_folders = last_step["step6_trim_intervals"].get("trimmed_folders", [])
    last_step["step6_trim_intervals"]["trimmed_folders"] = trimmed_folders

    for session_folder in session_folders:
        if session_folder in trimmed_folders:
            continue
            
        # e.g. "D:\\...\\20251103_1 session"
        # The prompt says: DS_cue = session.split(" ")[-1]
        DS_cue = session_folder.split(" ")[-1]
        if DS_cue not in ["DS+","DS-"]:
            continue # Skip trimming if not DS+ or DS- (e.g. session)

        videos = list_filespaths(session_folder)
        try:
            trim_DS_auto(videos, first=DS_cue, start_time=16, interval_duration=90, batch_size=5) # no need to save progress for each of DS+, DS- & CS+
        except Exception as e:
            error(f"Error trimming {session_folder}: {e}")
            
        trimmed_folders.append(session_folder)
        assignval("salvage_processing_step", last_step)

    assignval("salvage_processing_step", {
        "step7_apply_markers_and_move": {
            "session_folders": session_folders,
            "room": room
        }
    })
    
    return step7_apply_markers_and_move()

def step7_apply_markers_and_move():
    last_step = findval("salvage_processing_step")
    if "step7_apply_markers_and_move" not in last_step:
        error("Error finding last saved step. Starting over.")
        assignval("salvage_processing_step", {}) # Clear state
        continuous_process()
        return

    session_folders = last_step["step7_apply_markers_and_move"]["session_folders"]
    room = last_step["step7_apply_markers_and_move"]["room"]
    created_marked_videos = last_step["step7_apply_markers_and_move"].get("created_marked_videos", [])
    last_step["step7_apply_markers_and_move"]["created_marked_videos"] = created_marked_videos
    created_marker_folders = last_step["step7_apply_markers_and_move"].get("created_marker_folders", {})
    last_step["step7_apply_markers_and_move"]["created_marker_folders"] = created_marker_folders

    final_outputpath = find_folder_path("3-PROCESSED")    

    msgbox(f"PROBLEMATIC SESSION FOLDERS: {', '.join(created_marker_folders.keys())}\n\nPROBLEMATIC VIDEOS: {', '.join(created_marked_videos)}\n\nIf any videos or sessions are listed here, please review the marked videos and move them to the appropriate folders in 3-PROCESSED (with correct naming) before proceeding.\n\nClick OK to open the folder containing the marked videos.", title="Review Marked Videos")
    for session_folder in session_folders:
        basename = os.path.basename(session_folder)
        # Create folder for marked videos inside the session folder (temp)
        if session_folder not in created_marker_folders.keys():
            marked_folder = makefolder(final_outputpath, basename, start_at_1=False)
            created_marker_folders[session_folder] = marked_folder
            assignval("salvage_processing_step", last_step)
        else:
            marked_folder = created_marker_folders[session_folder]
        
        for vid in list_filespaths(session_folder):
             # markersquick.apply_png_overlay
            if vid in created_marked_videos:
                 continue
            
            apply_png_overlay(vid, marked_folder, room)
            created_marked_videos.append(vid)
            assignval("salvage_processing_step", last_step)
            
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

        # override_first_cue = True if custom_dialog("Separate each video into DS+/DS- intervals (for training only)?", title="Specify first cue for each session?") == "yes" else False
        override_first_cue = False

        grouped_recordings = group_by_date_and_sessionTime(recordings_folder,max_pause=750,warn_for_lost_time=True)

        assignval("salvage_processing_step", {"step1_organize_recordings_DATASAVE": 
                                              {"recordings_folder": recordings_folder, 
                                               "grouped_recordings": grouped_recordings,
                                               "override_first_cue": override_first_cue}})
        step1_organize_recordings_DATASAVE()
    else:
        answer = custom_dialog("An incomplete process has been found, continue?","continue interrupted process",op1="YES, continue.",op2="no")
        if answer != "YES, continue.":
            last_step = findval("salvage_processing_step")
            stepname = list(last_step.keys())[0]
            session_folders = last_step[stepname].get("session_folders")
            recordings_folder = last_step[stepname].get("recordings_folderpath")
            created_marker_folders = last_step[stepname].get("created_marker_folders")
            if created_marker_folders: # step 7
                if custom_dialog("Are you sure? This will delete the marked videos and you will need to re-mark them","warning",op1="delete",op2="Cancel") == "delete":
                    for folder in created_marker_folders.values():
                        walk_delete(folder)
                    for folder in session_folders:
                        walk_delete(folder)
                    assignval("salvage_processing_step", {})
                    continuous_process()
                    return
            elif session_folders: #step 3,4,5,6
                if custom_dialog("Are you sure? This will delete the video recordings and you will need to transfer the videos from the LOREX software again","warning",op1="delete",op2="Cancel") == "delete":
                    for folder in session_folders:
                        walk_delete(folder)
                    assignval("salvage_processing_step", {})
                    continuous_process()
                    return
                
            # If we reached here without returning, handle recording_folder logic
            recordings_folder = last_step[stepname].get("recordings_folder")
            if recordings_folder: #step 1,2
                print(f"{recordings_folder=}")
                assignval("salvage_processing_step", {}) 
                if os.path.exists(recordings_folder):
                    if custom_dialog(f"Restart process using the same folder?\n\n{recordings_folder=}", title="Transfer videos",dimensions=(450,250)) == "yes":
                        continuous_process(recordings_folder=recordings_folder)
                        return
            else:
                pass

            assignval("salvage_processing_step", {})
            continuous_process() #otherwise
            return

        # Only execute if we haven't restarted/returned
        current_step_data = findval("salvage_processing_step")
        if current_step_data:
            last_command = list(current_step_data.keys())[0]
            try:
                exec(f"{last_command}()")
            except Exception as e:
                error(f"Error executing {last_command}: {e}")

if __name__ == "__main__":
    continuous_process()