from common.common import *
import pandas, os
from os.path import splitext,basename

def start_trimming():
    # chosen_excel = select_anyfile("Select any excel file from detection results",specific_ext="xlsx")
    chosen_excel = r"C:\Users\matts\Downloads\test\01-20250925\light BL_all_centers.xlsx"
    if not chosen_excel:
        return
    detection_dir = os.path.dirname(os.path.dirname(chosen_excel))
    excel_files = [{"vid":basename(dirpath), "excels":[os.path.join(dirpath,f) for f in list_files_ext(dirpath,"xlsx")]} for dirpath in list_folderspaths(detection_dir)]
    for file in excel_files:
        if "~" in file:
            raise Exception("An excel file is opened. Please close all excel windows, then start this program again")


    # videos_to_trim = select_anyfile("Select the video files corresponding to detection results",specific_ext="mp4")
    videos_to_trim = [r"C:\Users\matts\Downloads\01-20250925.mp4"]
    if not videos_to_trim:
        return
    vid_dir = os.path.dirname(videos_to_trim[0])
    mp4_in_dir = list_files_ext(vid_dir,"mp4")
    if len(videos_to_trim) != len(mp4_in_dir):
        action = custom_dialog(f"You did not select all the videos ({len(videos_to_trim)}/{len(mp4_in_dir)} inside of {vid_dir}",op1="Continue with selected videos",op2=f"Select all videos in {os.path.basename(vid_dir)}")
        if action != "Continue with selected videos":
            videos_to_trim = list_files_ext(vid_dir,"mp4")

    paired_detection_and_vids = []
    for vid in videos_to_trim:
        for excel_file in excel_files:
            if splitext(basename(vid))[0] == excel_file["vid"]:
                paired_detection_and_vids.append({"vid":vid, "excels":excel_file["excels"]})
    
    for paired in paired_detection_and_vids:
        vidpath = paired["vid"]
        lights_xlsx = [os.path.join(detection_dir,excel) for excel in paired["excels"] if "light" in excel.lower()]

        light_presence = [step1_detector_excel_to_object_times(light_xlsx) for light_xlsx in lights_xlsx]
        
        print(light_presence)



    


def step1_detector_excel_to_object_times(excel_path: str) -> dict[str, list[dict[str, int]]]:
    """

    Returns: 
        keys are object names
        {"cue CS+": [
            {"first_frame": ..., "frame_duration": ..., "last_frame": ...},
            ...
            ]}
    """
    detector_data = {}
    try:
        df = pandas.read_excel(excel_path, sheet_name=None)  # Read all sheets
        object_name = os.path.basename(excel_path).replace("_all_centers.xlsx", "") # ex: "lever_right_all_centers.xlsx" -> "FNCL"
        
        for sheet_df in df.values():
            events = []
            
            # Get column B (index 1) values
            column_b_values = sheet_df.iloc[:, 1] 
            
            # Track groups of consecutive non-blank values
            current_group_start = None
            blank_space_start = None
            blank_space_count = 0
            
            for idx, value in enumerate(column_b_values):
                if pandas.notna(value) and str(value).strip() != '':  # Non-blank value
                    if current_group_start is None:
                        # Start of a new group
                        current_group_start = idx + 1  # +1 because Excel rows are 1-indexed
                        blank_space_start = None
                        blank_space_count = 0
                    elif blank_space_start is not None:
                        # We were in a blank space, check if it's less than 2
                        if blank_space_count < 2:
                            # Merge with previous group - continue the current group
                            blank_space_start = None
                            blank_space_count = 0
                        else:
                            # Blank space is 2 or more, end previous group and start new one
                            last_frame = blank_space_start - 1  # Last non-blank before the blank space
                            first_frame = current_group_start
                            frame_duration = last_frame - first_frame + 1
                            
                            events.append({
                                'first_frame': first_frame,
                                'last_frame': last_frame,
                                'frame_duration': frame_duration
                            })
                            
                            # Start new group
                            current_group_start = idx + 1
                            blank_space_start = None
                            blank_space_count = 0
                else:  # Blank value
                    if current_group_start is not None and blank_space_start is None:
                        # Start counting blank space
                        blank_space_start = idx + 1  # +1 for Excel row numbering
                        blank_space_count = 1
                    elif blank_space_start is not None:
                        # Continue counting blank space
                        blank_space_count += 1
            
            # Handle case where the last group extends to the end of the column
            if current_group_start is not None:
                if blank_space_start is not None and blank_space_count >= 2:  # ISSUE right now: when rat covers CL: considered as two different trials when no longer covers vs before covering (when it is the same in actuality)
                    # End the group before the blank space
                    last_frame = blank_space_start - 1
                else:
                    # Include everything up to the end
                    last_frame = len(column_b_values)
                
                first_frame = current_group_start
                frame_duration = last_frame - first_frame + 1
                
                # Only add if frame_duration is positive
                if frame_duration > 0:
                    events.append({
                        'first_frame': first_frame,
                        'last_frame': last_frame,
                        'frame_duration': frame_duration
                    })            
            detector_data[object_name.replace("_all_centers",'')] = events

    except Exception as e:
        raise(Exception(f"Error processing detector Excel file '{excel_path}': {e}"))
    
    return detector_data

start_trimming()