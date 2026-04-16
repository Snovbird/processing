from common.common import *
import pandas, os

def start_trimming():
    detectorResults_folder = select_folder("Select folder containing detection result folders")
    if not detectorResults_folder:
        return
    
    videos_to_trim = select_folder("Select a folder with the corresponding videos")

    # verify if mixed up the two folders:
    mp4_in_detector  = len(list_files_ext(detectorResults_folder, "mp4"))
    mp4_in_videos    = len(list_files_ext(videos_to_trim, "mp4"))
    xlsx_in_detector = len(list_files_ext(detectorResults_folder, "xlsx"))
    xlsx_in_videos   = len(list_files_ext(videos_to_trim, "xlsx"))

    if mp4_in_detector < mp4_in_videos and xlsx_in_detector > xlsx_in_videos: # ok
        videos = list_filespaths(videos_to_trim)
        detectorResults = list_filespaths(detectorResults_folder)
    elif mp4_in_videos == 0 and xlsx_in_detector == 0: # mixed up the two
        videos = list_filespaths(detectorResults_folder) 
        detectorResults = list_filespaths(videos_to_trim)
    else:
        error("Make sure you selected a parent folder with detection results FOLDERS inside, which is a file named '1-RAT_all_centers.xlsx'.\nYou also need the prepared videos from '3-PROCESSED'")



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



