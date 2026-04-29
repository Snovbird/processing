from common.common import grid_selector
from common.common import askstring
from adjuster.dependencies import list_files
from common.common import *
import pandas, os,datetime, json
from os.path import splitext,basename
from newtrim import batch_trim
from concatenate import concatenate
from TRIM import trim_frames

class trimObtainIntervals():
    def __init__(self,detection_results_dir:str = None,videos_to_trim:list[str]=None):
        self.detection_results_dir = detection_results_dir
        if not self.detection_results_dir:
            chosen_excel:str = select_anyfile("Select any excel file from detection results",specific_ext="xlsx")[0]
            self.detection_results_dir = os.path.dirname(os.path.dirname(chosen_excel))
            if len(list_files(self.detection_results_dir)) > 0:
                raise ValueError(f"Invalid results directory. Make sure there are only folders containing detection results in {self.detection_results_dir}")
        
        self.videos_to_trim = videos_to_trim            
        if not self.videos_to_trim:
            chosen_mp4s:list[str] = select_anyfile("Select the video files corresponding to detection results",specific_ext="mp4")
            mp4_dir = os.path.dirname(chosen_mp4s[0])
            all_files_in_mp4_dir = list_files_ext(mp4_dir,"mp4",fullpath=True)
            len_chosen = len(chosen_mp4s)
            len_all = len(all_files_in_mp4_dir)
            if len_chosen != len_all:
                action = custom_dialog(f"You did not select all the videos ({len_chosen}/{len_all}) inside of {mp4_dir}",op1="Continue with selected videos",op2=f"Select all videos in {os.path.basename(os.path.dirname(chosen_mp4s[0]))}")
                if action == "Continue with selected videos":
                    self.videos_to_trim = chosen_mp4s
                else:
                    self.videos_to_trim = all_files_in_mp4_dir
            else: # its all the videos in the dir
                self.videos_to_trim = chosen_mp4s

        self.excel_files = [{"vid":basename(dirpath), "excels":[os.path.join(dirpath,f) for f in list_files_ext(dirpath,"xlsx")]} for dirpath in list_folderspaths(self.detection_results_dir)]
        for file in self.excel_files:
            if "~" in file:
                raise Exception("An excel file is opened. Please close all excel windows, then start this program again")
        self.output_folder_name = askstring("Enter the name of the output folder containing the trimmed videos ready for analysis")
        self.output_folder = makefolder(os.path.dirname(self.videos_to_trim[0]), self.output_folder_name, start_at_1=False)
        self.cuepositionnames = set([basename(xlsx).split("_")[2] for xlsx in self.excel_files[0]["excels"] if "rat" not in xlsx.lower() and "light" in xlsx]) # 1_light_BL_all_centers
        self.cuepositionnames = list(self.cuepositionnames)
        self.cuepositionnames.sort()
        self.corresponding_cuenames = grid_selector(self.cuepositionnames,options_list=["DS+","DS-","CS+","CS-"],
                                                message="Select corresponding cue names to the position name",
                                                title="Corresponding Cue Names")
        self.cue_folders = {cue: makefolder(self.output_folder,cue,start_at_1=False) for cue in self.corresponding_cuenames.values()}
            
            
        self.paired_vids_with_excel = []
        self.object_presence = []
        self.separated_presence = []
        self.with_merged_light_presence = []
        self.with_clean_lever_data = []
        self.trimmed_mp4s = []
        self.primetrial = []
        self.times_minus_ITI = []
        self.to_reassemble = []
        self.concatenated = []
        

    def s1_pair_vids_with_excel(self):
        for vid in self.videos_to_trim:
            for excel_file in self.excel_files:
                if splitext(basename(vid))[0] == excel_file["vid"]:
                    self.paired_vids_with_excel.append({"vid":vid, "excels":excel_file["excels"]})
        return self.paired_vids_with_excel
    
    def s2_object_times(self):
        if not self.paired_vids_with_excel:
            self.s1_pair_vids_with_excel()
        
        for vid_excel in self.paired_vids_with_excel:
            vid = vid_excel["vid"]
            excels = vid_excel["excels"]
            obj_presence_xlsx = [xlsx for xlsx in excels if "rat" not in xlsx.lower()]
            obj_presence_data = [detector_excel_to_object_times(xlsx,minblank=2) for xlsx in obj_presence_xlsx]

            self.object_presence.append(
                {
                    "vid": vid,
                    "data": obj_presence_data
                }
            )
    
    def s3_adjust_data(self,minblank:int = 0):
        """
        (1) separate light from lever presence data
        (2) adjust data groups contents to remove blank groups to obtain:
            {
                "object": object_name,
                "first_frame": presence_group["first_frame"],
                "duration": presence_group["duration"],
                "last_frame": presence_group["last_frame"]
            }
        (3) Provide a list of dicts of both light and presence data separately
        """
        if not self.object_presence:
            self.s2_object_times()
        
        for vid_data in self.object_presence:
            vid = vid_data["vid"]
            obj_presence_data = vid_data["data"]

            lever_presence_data:list[list[dict]] = [adjust_blank(data["object"],data["data"],minblank=minblank) for data in obj_presence_data if "lever" in data["object"]]
            light_presence_data:list[list[dict]] = [adjust_blank(data["object"],data["data"],minblank=minblank) for data in obj_presence_data if "light" in data["object"]]
            
            minimum_light_duration = 3
            light_presence_data, light_problematic = light_min_duration(light_presence_data,min_duration=minimum_light_duration)
            if light_problematic:
                frame_numbers = "\n".join([str(x) for x in light_problematic])
                error(f"Light presence data for {vid} had {len(light_problematic)} instances where the duration was less than {minimum_light_duration} frames.\n{frame_numbers}\n\nOccurences:\n{frame_numbers}")

            combined_light_data: list[dict] = [item for data in light_presence_data for item in data]
            combined_lever_data: list[dict] = [item for data in lever_presence_data for item in data]
            
            self.separated_presence.append(
                {
                    "vid": vid,
                    "lever": combined_lever_data,
                    "light": combined_light_data
                }
            )
        return self.separated_presence

    def s4_merge_light_presence(self):
        if not self.separated_presence:
            self.s3_adjust_data()
        
        
        for vid_data in self.separated_presence:
            vid = vid_data["vid"]
            light_data = vid_data["light"]
            lever_data = vid_data["lever"]

            clean_light_data = merge_light_presence(light_data)

            self.with_merged_light_presence.append(
                {
                    "vid": vid,
                    "lever": lever_data,
                    "light": clean_light_data
                }
            )
        return self.with_merged_light_presence
    
    def s5_combined_lever_data(self,min_lever_detection:int = 2):
        if not self.with_merged_light_presence:
            self.s4_merge_light_presence()
        
        for vid_data in self.with_merged_light_presence:
            vid = vid_data["vid"]
            lever_data = vid_data["lever"]
            clean_light_data = vid_data["light"]

            clean_lever_data = clean_lever_presence(lever_presence=lever_data,
                light_presence=clean_light_data,
                min_detection_duration_frames=min_lever_detection)

            self.with_clean_lever_data.append(
                {
                    "vid": vid,
                    "lever": clean_lever_data,
                    "light": clean_light_data
                }
            )
        return self.with_clean_lever_data

    def s6_primetrial(self):
        if not self.with_clean_lever_data:
            self.s5_combined_lever_data()

        for timeseries in self.with_clean_lever_data:
            vid = timeseries["vid"]
            lever_times = timeseries["lever"]
            light_times = timeseries["light"]

            primetrial = obtain_primetrial_intervals(light_times,lever_times)
            # value example = {"interval":f"DS+ prime", "first_frame": 100, "last_frame": 150}
            self.primetrial.append(
                {
                    "vid": vid,
                    "intervals": primetrial
                }
            )
        return self.primetrial
        
    def s7_trim_for_analysis(self):
        if not self.primetrial:
            self.s6_primetrial()

        for timeseries in self.primetrial:
            vid = timeseries["vid"]
            self.to_reassemble.append({cue: [] for cue in self.corresponding_cuenames.values()})
            intervals:list[dict[str,str|int]] = timeseries["intervals"]
            for interval in intervals:

                positionname = interval["interval_name"].split(" ")[0]
                corresponding_cue = self.corresponding_cuenames[positionname]
                cue_folder = self.cue_folders[corresponding_cue]

                start_time = interval["first_frame"]
                end_time = interval["last_frame"] + 1
                interval_name = interval["interval_name"]
                outpath = trim_frames(vid,start_time=start_time,end_time=end_time,output_folder=cue_folder,show_terminal=False)
                self.to_reassemble[-1][corresponding_cue].append({
                    "snippet_path": outpath, 
                    "interval_name": interval_name,
                    "first_frame": interval["first_frame"],
                    "duration": interval["duration"],
                    "last_frame": interval["last_frame"]
                })

        return self.to_reassemble
    

    def s8_reassemble_separated(self):
        """
        concatenate
        """
        if not self.to_reassemble:
            self.s7_trim_for_analysis()
        
        for cue_vidsprops in self.to_reassemble:
            for cue, vidsprops in cue_vidsprops.items():
                
                vids = [vidprop["snippet_path"] for vidprop in vidsprops]
                interval_names_and_times = [{"interval_name": vidprop["interval_name"],
                                             "first_frame": vidprop["first_frame"],
                                             "duration": vidprop["duration"],
                                             "last_frame": vidprop["last_frame"]} for vidprop in vidsprops]

                
                output = concatenate(vids,output_folder=self.output_folder)
                oldname,ext = splitext(basename(output))
                newname = f"{oldname} {cue}{ext}"
                newpath = os.path.join(self.output_folder,newname)
                os.rename(output,newpath)
                
                self.concatenated.append({
                    "path": newpath,
                    "intervals": interval_names_and_times
                })
                
        return self.concatenated

    def s9_times_minus_ITI(self): # to complete
        
        if not self.concatenated:
            self.s8_reassemble_separated()
        
        for concat_interval in self.concatenated:
            concatenated_video = concat_interval["path"]
            intervals = concat_interval["intervals"]

            minus_ITI = times_minus_ITI(intervals)

            self.times_minus_ITI.append({
                "path": concatenated_video,
                "intervals": minus_ITI
            })
        return self.times_minus_ITI
    
    def s10_export_data_json(self,):
        if not self.times_minus_ITI:
            self.s9_times_minus_ITI()

        with open(os.path.join(self.output_folder,"interval_times_and_names.json"), "w") as f:
            json.dump(self.times_minus_ITI, f, indent=4)
            


def detector_excel_to_object_times(excel_path: str,minblank: int) -> dict[str, str | list[dict[str, int]]]:
    """
    Args:
        excel_path: path to an excel file containing detector results for an object (ex: "C:\...\light BL_all_centers.xlsx")
        minblank: min number of consecutive frames to consider an object to be no longer present. Eg: minblank=2 and we have: 6-frame BL_light presence, then 1 blank frame, then 5 frames of BL_light presence. This would be considered as one continuous presence of BL_light for 12 frames (6+1+5) because the blank frame is less than minblank. If there were 2 or more consecutive blank frames, then it would be considered as two separate presences of BL_light (one for the first 6 frames, and one for the last 5 frames).

    Returns: {"object":"light BL",
        "data": [{"first_frame": ..., "duration": ..., "last_frame": ...}, ... ]}
    """
    df = pandas.read_excel(excel_path, sheet_name=None)  # Read all sheets
    interval_object_name = os.path.basename(excel_path).split("_")[1:-2] # ex: "lever_right_all_centers.xlsx" -> ["lever", "right"]
    if len(interval_object_name) != 2:
        raise ValueError(f"Unexpected object name in excel file: {interval_object_name}.\nShould be named as 1_light_Bl_all_centers.xlsx")
    
    for sheet in df.values():
        obj_detection_result = sheet.iloc[:, 1] # column B (index 1) 

        obj_presence_data = []
        object_is_present = False
        first_frame_of_presence = True

        for frame_number, data_value in enumerate(obj_detection_result):
            if pandas.notna(data_value):  # Non-blank value
                if not object_is_present:
                    # Start of a new presence
                    object_is_present = True
                    obj_presence_data.append({"present": True, "first_frame": frame_number, "duration": 1})
                    first_frame_of_presence = False
                elif object_is_present:
                    # Continue the current presence
                    obj_presence_data[-1]["duration"] += 1
            else:
                if first_frame_of_presence:
                    obj_presence_data.append({"present": False, "first_frame": frame_number, "duration": 1})
                    first_frame_of_presence = False
                    object_is_present = False
                elif object_is_present: # start a new present: False group
                    obj_presence_data.append({"present": False, "first_frame": frame_number, "duration": 1})
                    object_is_present = False
                elif not object_is_present:
                    obj_presence_data[-1]["duration"] += 1
                

        return {"object" : " ".join(interval_object_name),
                "data": obj_presence_data}

def adjust_blank(object_name:str, presence_data: list[dict[str, int]], minblank: int = 0, removeblank = True) -> list[dict[str, int]]:
    """
    Remove blank groups and extend object presence by merging blank sequences SHORTER (<) than minblank and the following object presence group. Adds last_frame key using the following operation: first frame + duration - 1Ex: {"present": True, "first_frame": 10, "duration": 6}, {"present": False, "first_frame": 17, "duration": 1}, {"present": True, "first_frame": 18, "duration": 5} would be merged into {"present": True, "first_frame": 10, "duration": 12} if minblank is 2 or more, but would not be merged if minblank is 1 or less.
    Args:
        presence_data: output of step1_detector_excel_to_object_times for a single object. Ex: [{"present": True, "first_frame": 10, "duration": 5}, {"present": False, "first_frame": 15, "duration": 1}, {"present": True, "first_frame": 16, "duration": 4}, ...]
        minblank: min number of consecutive frames to consider an object to be no longer present. Eg: minblank=2 and we have: 6-frame BL_light presence, then 1 blank frame, then 5 frames of BL_light presence. This would be considered as one continuous presence of BL_light for 12 frames (6+1+5) because the blank frame is less than minblank. If there were 2 or more consecutive blank frames, then it would be considered as two separate presences of BL_light (one for the first 6 frames, and one for the last 5 frames).

    Returns:
        presence data with short blanks merged into presences. E.g. [{"present": True, "first_frame": 10, "duration": 12}, ...]
    """
    
    merged_presence = []
    merged_previous = False
    for presence_group in presence_data:
        if presence_group["present"]:
            if not merged_previous:
                newgroup = {
                    "object": object_name,
                    "first_frame": presence_group["first_frame"],
                    "duration": presence_group["duration"],
                    "last_frame": presence_group["first_frame"] + presence_group["duration"] - 1
                }

                merged_presence.append(newgroup)
            elif merged_previous:
                merged_presence[-1]["duration"] += presence_group["duration"]
                merged_presence[-1]["last_frame"] = presence_group["first_frame"] + presence_group["duration"] - 1
                merged_previous = False

        elif not presence_group["present"]:
            if presence_group["duration"] < minblank:
                merged_presence[-1]["duration"] += presence_group["duration"]
                merged_presence[-1]["last_frame"] = presence_group["first_frame"] + presence_group["duration"] - 1 # in case it ends with a <minblank
                merged_previous = True
            else:
                if not removeblank:
                    merged_presence.append(presence_group)
                    merged_presence[-1]["is blank"] = True # new value added
                else:
                    pass

    return merged_presence

def light_min_duration(presence:list[dict], min_duration):

    new_presence = []
    problematic = []
    for data in presence:

        if data["duration"] >= min_duration:

            new_presence.append(data)
        else:
            problematic.append(data["first_frame"])

    return new_presence, problematic


def merge_light_presence(light_data: list[dict[str, int]],) -> list[dict[str, int]]:
    """
    Sorts in order of first_frame and merges consecutive intervals with the same object present (ex: rat covers cue light so two DS+ intervals are consecutive)
    """


    light_data.sort(key= lambda x: x["first_frame"])

    new_light_data = []
    for n,data in enumerate(light_data):
        
        previous = light_data[n-1] if n != 0 else None
        previous_object = previous["object"] if previous else None

        if data["object"] == previous_object: # two of the same cue follows each other = rat covered light --> merge them!
            new_light_data[-1]["duration"] = data["last_frame"] - previous["first_frame"]
            new_light_data[-1]["last_frame"] = data["last_frame"]
        else: # a different cue (which is expected)
            new_light_data.append(data)
    
    return new_light_data

def merge_lever_presence(lever_presence: list[dict[str, int]], light_presence: list[dict[str, int]], max_delay: int) -> list[dict[str, int]]:
    """
    Args:
        lever_presence: output of step2_remove_blanks_and_merge_short for the lever. Ex: [{"present": True, "first_frame": 10, "duration": 12}, ...]
        light_presence: output of step2_remove_blanks_and_merge_short for the light. Ex: [{"present": True, "first_frame": 8, "duration": 5}, ...]
        max_delay: max number of frames between a light presence and a lever presence for them to be considered as related. Eg: max_delay=2 and we have a light presence from frames 8 to 12, and a lever presence from frames 13 to 20. The lever presence would be extended to start at frame 8 (instead of 13) because the delay between the light presence and the lever presence is only 1 frame (which is less than max_delay). If the lever presence started at frame 15 instead of 13, it would not be extended because the delay would be 3 frames (which is more than max_delay).
    """

    lever_presence.sort(key=lambda x: x['first_frame']) # sort by first_frame of presence
    lever_presence = [group for group in lever_presence] # if group['duration'] >= min_detection_duration_frames] # remove short detections - UNUSED
    
    def add_durations(group1,group2):
        first_frame = min(group1['first_frame'], group2['first_frame'])
        last_frame = max(group1['last_frame'], group2['last_frame'])
        duration = last_frame - first_frame + 1
        return {"first_frame": first_frame, "last_frame": last_frame, "duration": duration}

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

def clean_lever_presence(lever_presence: list[dict[str, int]],light_presence: list[dict[str, int]], min_detection_duration_frames: int = 3) -> list[dict[str, int]]:
    """
    Removes lever presence that is not associated with a light presence. Ignores groups of lever presence under min_detection_duration_frames (default is 3)
    """
    clean_lever_presence = []
    for nl, lever_group in enumerate(lever_presence):
        if lever_group['duration'] < min_detection_duration_frames:
            continue
        last_levergroup_first_frame = lever_presence[nl-1] if nl > 0 else -1
        for nc, cue_group in enumerate(light_presence):
            next_cuegroup_first_frame = light_presence[nc+1]['first_frame'] if nc != len(light_presence)-1 else float('inf')
            if lever_group['first_frame'] > cue_group['last_frame']:
                continue # the cue turns OFF before the lever extends -> move to next cue illumination
            elif cue_group['first_frame'] <= lever_group['first_frame'] < next_cuegroup_first_frame: # lever extends after cue turns ON
                if lever_group['first_frame'] < cue_group['last_frame']:
                    

                    clean_lever_presence.append(
                        {"first_frame": lever_group['first_frame'], 
                        "last_frame": cue_group['last_frame'], # the lever supposed to retract at the same time as the light turns OFF 
                        "duration": cue_group['last_frame'] - lever_group['first_frame'] + 1}
                    )
                break # lever retracts --> no need to continue iterating through cue illuminations 

    return clean_lever_presence

def obtain_primetrial_intervals(light_presence,lever_presence):
    intervals:list[ dict[str,str|int] ] = []
    for cuegroup in light_presence:
        for lever_group in lever_presence:
            if cuegroup['last_frame'] < lever_group['first_frame']:
                break # cue turns OFF --> no need to continue iterating through lever extensions 
            elif cuegroup['first_frame'] > lever_group['last_frame']:
                continue # the lever retracted before the cue becomes illuminated --> move to next extension
                
            if cuegroup['first_frame'] <= lever_group['first_frame'] < cuegroup['last_frame']: # if lever is present while cue is illuminated, we have a trial interval!
                prime_interval_start = cuegroup['first_frame']
                trial_interval_start = lever_group['first_frame'] 
                trial_interval_end = cuegroup['last_frame']
                trial_duration = trial_interval_end - trial_interval_start + 1
                cue = cuegroup["object"].split(" ")[1] # ex: "light BL" --> "BL"

                # prime
                prime_duration = trial_interval_start - prime_interval_start
                intervals.append({"interval_name":f"{cue} prime", "first_frame": prime_interval_start, "duration": prime_duration, "last_frame": trial_interval_start - 1})

                # trial
                trial_duration = trial_interval_end - trial_interval_start + 1
                intervals.append({"interval_name":f"{cue} trial", "first_frame": trial_interval_start, "duration": trial_duration, "last_frame": trial_interval_end})

    intervals.sort(key=lambda x: x['first_frame']) # sort by first_frame of interval
    
    #cleanup short lever presence?

    return intervals

def times_minus_ITI(intervals:list):
    minus_ITI = []    

    for n, interval in enumerate(intervals):
        if n == 0:
            minus_ITI.append(interval) 
            continue
        last_endtime = minus_ITI[-1]["last_frame"]

        new_first = last_endtime + 1
        duration = interval["duration"] 
        new_last = new_first + duration -1

        minus_ITI.append({"interval_name":interval["interval_name"], "first_frame":new_first, "last_frame":new_last, "duration": duration})
        
    return minus_ITI

if __name__ == "__main__":
    # test = trimObtainIntervals(detection_results_dir=r"C:\Users\samahalabo\Desktop\10-ANALYSIS\20260423 detector")
    # test.s9_times_minus_ITI()
    det = detector_excel_to_object_times(r"C:\Users\samahalabo\Desktop\10-ANALYSIS\20260423 detector\03-20260411-140647-140708-140734-143000-143000-145939\6_light_FR_all_centers.xlsx",minblank=0)
    
    clean = adjust_blank(object_name="light FR", presence_data=det["data"], minblank=2)
    clean2 = light_min_duration(clean,min_duration=3)
    
    for group in clean2:
        print(group)
