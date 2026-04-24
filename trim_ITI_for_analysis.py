from common.common import *
import pandas, os
from os.path import splitext,basename
from newtrim import batch_trim
from concatenate import concatenate


class trimObtainIntervals():
    def __init__(self,detection_results_dir:str = None,videos_to_trim:list[str]=None):
        self.detection_results_dir = detection_results_dir
        if not self.detection_results_dir:
            chosen_excel = select_anyfile("Select any excel file from detection results",specific_ext="xlsx")
            self.detection_results_dir = os.path.dirname(chosen_excel)
        self.videos_to_trim = videos_to_trim
        if not self.videos_to_trim:
            self.videos_to_trim = select_anyfile("Select the video files corresponding to detection results",specific_ext="mp4")
    
    detection_dir = os.path.dirname(os.path.dirname(chosen_excel))
    excel_files = [{"vid":basename(dirpath), "excels":[os.path.join(dirpath,f) for f in list_files_ext(dirpath,"xlsx")]} for dirpath in list_folderspaths(detection_dir)]
    for file in excel_files:
        if "~" in file:
            raise Exception("An excel file is opened. Please close all excel windows, then start this program again")

    
    # videos_to_trim = select_anyfile("Select the video files corresponding to detection results",specific_ext="mp4")
    videos_to_trim = [r"C:\Users\matts\Downloads\01-20250925.mp4"]

    output_path = select_folder("Choose an empty directory where to place the trimmed videos")

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
    
    intervals_per_vid = []
    for vid_excel in paired_detection_and_vids:
        vid = vid_excel["vid"]
        obj_presence_xlsx = [xlsx for xlsx in vid_excel["vid"] if "rat" not in xlsx.lower()]

        obj_presence_data = [detector_excel_to_object_times(xlsx) for xlsx in obj_presence_xlsx]

        lever_presence_data:list[list[dict]] = [adjust_blank(data["object"],data["data"]) for data in obj_presence_data if "lever" in data["object"]]
        light_presence_data:list[list[dict]] = [adjust_blank(data["object"],data["data"]) for data in obj_presence_data if "light" in data["object"]]
        combined_light_data:list[dict] = []
        for i in light_presence_data:
            combined_light_data.extend(i)

        clean_light_data = merge_light_presence(combined_light_data)

        data_per_light:dict[str,int] = {}
        for data in clean_light_data:
            light_intervals = data_per_light.get(data["object"],[])
            light_intervals.append(
                {
                    "start frame":data["start frame"],
                    "duration": data["duration"],
                    "last frame": data["last frame"]
                }
            )
            
        for light,intervals in data_per_light.items():
            light_folder = makefolder(output_path,light,start_at_1=False)
            start_times = []
            end_times = []
            for interval in intervals:
                start_times.append(interval["start frame"])
                end_times.append(interval["last frame"])
            
            files_to_concatenate = batch_trim(vid, start_times, end_times, output_folder=light_folder)
            files_to_concatenate.sort()
            output = concatenate(files_to_concatenate,output_folder=output_path,override_output_name=f"{light} {len(intervals)} intervals")

            os.rename(output, os.path.join(output_path,f"{light} {len(intervals)} intervals.mp4"))
        else:
            os.startfile(output_path)


    # obtain clean lever data for analysis (later) and prime-trial differentiation    
        combined_lever_data = []
        for data in lever_presence_data:
            combined_lever_data.extend(data)

        clean_lever_data = merge_lever_presence(combined_lever_data)
        
        primetrial = obtain_primetrial_intervals(clean_light_data, clean_lever_data)
        
        intervals_per_vid.append(
            {
                "vid": vid,
                "intervals": primetrial
            }
        )

def detector_excel_to_object_times(excel_path: str,minblank: int) -> dict[str, str | list[dict[str, int]]]:
    """
    Args:
        excel_path: path to an excel file containing detector results for an object (ex: "C:\...\light BL_all_centers.xlsx")
        minblank: min number of consecutive frames to consider an object to be no longer present. Eg: minblank=2 and we have: 6-frame BL_light presence, then 1 blank frame, then 5 frames of BL_light presence. This would be considered as one continuous presence of BL_light for 12 frames (6+1+5) because the blank frame is less than minblank. If there were 2 or more consecutive blank frames, then it would be considered as two separate presences of BL_light (one for the first 6 frames, and one for the last 5 frames).

    Returns: 
        keys are object names
        {"light BL": [
            {"first_frame": ..., "frame_duration": ..., "last_frame": ...},
            ...
            ]}
    """
    df = pandas.read_excel(excel_path, sheet_name=None)  # Read all sheets
    interval_object_name = os.path.basename(excel_path).split("_")[1:-2] # ex: "lever_right_all_centers.xlsx" -> ["lever", "right"]
    if len(interval_object_name) != 2:
        raise ValueError(f"Unexpected object name in excel file: {interval_object_name}.\nShould be named as 1_light_Bl_all_centers.xlsx")
    
    sheet = df.values()[0]
    obj_detection_result = sheet.iloc[:, 1] # column B (index 1) 

    obj_presence_data = []
    object_is_present = False

    for frame_number, data_value in enumerate(obj_detection_result):
        if pandas.notna(data_value):  # Non-blank value
            if not object_is_present:
                # Start of a new presence
                object_is_present = True
                obj_presence_data.append({"present": True, "start frame": frame_number, "duration": 1})
            elif object_is_present:
                # Continue the current presence
                obj_presence_data[-1]["duration"] += 1
        else:
            if object_is_present:
                # End of the current presence
                object_is_present = False
                obj_presence_data.append({"present": False, "start frame": frame_number, "duration": 1})
            elif not object_is_present:
                obj_presence_data[-1]["duration"] += 1

    return {"object" : " ".join(interval_object_name),
             "data": obj_presence_data}

def adjust_blank(object_name:str, presence_data: list[dict[str, int]], minblank: int = 0, removeblank = True) -> list[dict[str, int]]:
    """
    Remove blank groups and extend object presence by merging blank sequences SHORTER (<) than minblank and the following object presence group. Ex: {"present": True, "start frame": 10, "duration": 6}, {"present": False, "start frame": 17, "duration": 1}, {"present": True, "start frame": 18, "duration": 5} would be merged into {"present": True, "start frame": 10, "duration": 12} if minblank is 2 or more, but would not be merged if minblank is 1 or less.
    Args:
        presence_data: output of step1_detector_excel_to_object_times for a single object. Ex: [{"present": True, "start frame": 10, "duration": 5}, {"present": False, "start frame": 15, "duration": 1}, {"present": True, "start frame": 16, "duration": 4}, ...]
        minblank: min number of consecutive frames to consider an object to be no longer present. Eg: minblank=2 and we have: 6-frame BL_light presence, then 1 blank frame, then 5 frames of BL_light presence. This would be considered as one continuous presence of BL_light for 12 frames (6+1+5) because the blank frame is less than minblank. If there were 2 or more consecutive blank frames, then it would be considered as two separate presences of BL_light (one for the first 6 frames, and one for the last 5 frames).

    Returns:
        presence data with short blanks merged into presences. E.g. [{"present": True, "start frame": 10, "duration": 12}, ...]
    """
    
    merged_presence = []
    merged_previous = False
    for presence_group in presence_data:
        if presence_group["present"]:
            if not merged_previous:
                newgroup = {
                    "object": object_name,
                    "first frame": presence_group["first frame"],
                    "duration": presence_group["duration"],
                    "last frame": presence_group["last frame"]
                }

                merged_presence.append(newgroup)
            elif merged_previous:
                merged_presence[-1]["duration"] += presence_group["duration"]
                merged_presence[-1]["last frame"] = presence_group["last frame"]
                merged_previous = False

        elif not presence_group["present"]:
            if presence_group["duration"] < minblank:
                merged_presence[-1]["duration"] += presence_group["duration"]
                merged_presence[-1]["last frame"] = presence_group["last frame"] # in case it ends with a <minblank
                merged_previous = True
            else:
                if not removeblank:
                    merged_presence.append(presence_group)
                    merged_presence[-1]["is blank"] = True # new value added
                else:
                    pass

    return merged_presence

def merge_light_presence(light_data: list[dict[str, int]],) -> list[dict[str, int]]:
    """
    Sorts in order of first frame and merges consecutive intervals with the same object present (ex: rat covers cue light so two DS+ intervals are consecutive)
    """


    light_data.sort(key= lambda x: x["first frame"])

    new_light_data = []
    for n,data in enumerate(light_data):
        
        previous = light_data[n-1] if n != 0 else None

        if data["object"] == previous["object"]: # two of the same cue follows each other = rat covered light --> merge them!
            new_light_data[-1]["duration"] = data["last frame"] - previous["first frame"]
            new_light_data[-1]["last frame"] = data["last frame"]
        else: # a different cue (which is expected)
            new_light_data.append(data)
    
    return new_light_data

def merge_lever_presence(lever_presence: list[dict[str, int]], light_presence: list[dict[str, int]], max_delay: int) -> list[dict[str, int]]:
    """
    Args:
        lever_presence: output of step2_remove_blanks_and_merge_short for the lever. Ex: [{"present": True, "start frame": 10, "duration": 12}, ...]
        light_presence: output of step2_remove_blanks_and_merge_short for the light. Ex: [{"present": True, "start frame": 8, "duration": 5}, ...]
        max_delay: max number of frames between a light presence and a lever presence for them to be considered as related. Eg: max_delay=2 and we have a light presence from frames 8 to 12, and a lever presence from frames 13 to 20. The lever presence would be extended to start at frame 8 (instead of 13) because the delay between the light presence and the lever presence is only 1 frame (which is less than max_delay). If the lever presence started at frame 15 instead of 13, it would not be extended because the delay would be 3 frames (which is more than max_delay).
    """

    lever_presence.sort(key=lambda x: x['first_frame']) # sort by first frame of presence
    lever_presence = [group for group in lever_presence if group['frame_duration'] >= min_detection_duration_frames] # remove short detections
    
    def add_durations(group1,group2):
        first_frame = min(group1['first_frame'], group2['first_frame'])
        last_frame = max(group1['last_frame'], group2['last_frame'])
        frame_duration = last_frame - first_frame + 1
        return {"first_frame": first_frame, "last_frame": last_frame, "frame_duration": frame_duration}

    # combine/ignore intersecting lever presence
    lever_presence = [add_durations(group, lever_presence[group_number+1]) # tldr: add durations if 2nd group ends after current group
                      if group_number + 1 < len(lever_presence) 
                      # if there is a next group
                      and lever_presence[group_number+1]["last_frame"] >= group["first_frame"] 
                      # and next group starts before current ends
                      and lever_presence[group_number+1]["first_frame"] <= group["last_frame"] 
                      # and next group ends after current starts (needs extending)
                      else group 
                      # otherwise keep current group that does not intersect with anything
                      for group_number, group in enumerate(lever_presence) 
                      if group_number == 0 # first group, so cannot index at [group_number-1]
                      or not (lever_presence[group_number-1]['last_frame'] >= group['first_frame'] # if current group starts after and ends before previous ends, ignore
                              and lever_presence[group_number-1]['first_frame'] <= group['last_frame'])
                              ] 
    return lever_presence

def obtain_primetrial_intervals(light_presence,lever_presence):
    intervals:list[ dict[str,str|int] ] = []
    for cue, cue_groups in light_presence.items():
        for cuegroup in cue_groups:
            for lever_groups in lever_presence:
                for lever_group in lever_groups:
                    if cuegroup['last_frame'] < lever_group['first_frame']:
                        break # cue turns OFF --> no need to continue iterating through lever extensions 
                    elif cuegroup['first_frame'] > lever_group['last_frame']:
                        continue # the lever retracted before the cue becomes illuminated --> move to next extension
                        
                    if cuegroup['first_frame'] <= lever_group['first_frame'] < cuegroup['last_frame']: # if lever is present during the cue presence
                        prime_interval_start = cuegroup['first_frame']
                        trial_interval_start = lever_group['first_frame'] 
                        trial_interval_end = cuegroup['last_frame']

                        intervals.append({"interval":f"{cue} prime", "first_frame": prime_interval_start, "last_frame": trial_interval_start})

                        intervals.append({"interval":f"{cue} trial", "first_frame": trial_interval_start, "last_frame": trial_interval_end})

    intervals.sort(key=lambda x: x['first_frame']) # sort by first frame of interval
    
    #cleanup short lever presence?

    return intervals

if __name__ == "__main__":
    trimObtainIntervals(detection_results_dir="C:/Users/matts/Downloads/test/",videos_to_trim=["C:/Users/matts/Downloads/01-20250925.mp4"])