from common.common import grid_selector
import json, os, pandas
from common.common import *
from excel.writer_complex import writer_complex 
from excel.general import fit_columns,excel_to_list
from excel.outdated.export import export_excel


def step0_pair_detectorExcels_analysisExcel(detectorResults_folder:str, analysisResults_folder:str) -> list[tuple[str,str]]:
    """
    Returns a tuple of ( {"analysisExcel_path.xlsx" : ["cue1.xlsx", "cue2.xlsx", ...], ...}, (obj1,obj2,...) )
    """
    
    paired_excels = {}
    while True:
        for analysisFolder, detectorFolder in zip(list_folderspaths(analysisResults_folder), list_folderspaths(detectorResults_folder)):
            if analysis_xlsx_list != list_files_ext(analysisFolder, "xlsx") or detector_xlsx_list != list_files_ext(detectorFolder, "xlsx"):
                raise(Exception(f"'{os.path.basename(analysisFolder)}' and '{os.path.basename(detectorFolder)}' do not contain the same detected objects. \nPlease check that the folders are all detection results in '{detectorResults_folder}'"))
            analysis_xlsx_list = list_files_ext(analysisFolder, "xlsx")
            detector_xlsx_list = list_files_ext(detectorFolder, "xlsx")
            if len(analysis_xlsx_list) > 1 and len(detector_xlsx_list) == 1: # mixed up the two
                error("Next time, choose the analysis results folder first, then the detector results folder","WARNING")
                saved_ana = analysisResults_folder
                analysisResults_folder:str = detectorResults_folder
                detectorResults_folder:str = saved_ana
                break
                
            
            if os.path.basename(analysisFolder) != os.path.basename(detectorFolder):
                raise(Exception(f"'{os.path.basename(analysisFolder)}' and '{os.path.basename(detectorFolder)}' are not the same video name. \nPlease check that the folders in '{analysisResults_folder}' and '{detectorResults_folder}' are the same."))
            paired_excels[os.path.join(analysisFolder, analysis_xlsx_list[0])] = [os.path.join(detectorFolder, f) for f in list_files_ext(detectorFolder, "xlsx")]
        else:
            break

    objects_in_detector = [object.replace("_all_centers.xlsx","") for object in detector_xlsx_list]
    return paired_excels, objects_in_detector

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

def step2_determine_interval_times_from_detector(detector_data: dict[str, list[dict[str, int]]],cues=["light_BL","light_BR","light_FR"],min_detection_duration_frames=3) -> dict[str, list[dict[str, int]]]:
    """
    min_detection_duration_frames: minimum (>=) number of frames of presence to be considered a valid interval (ex: 3 frames = 0.2 seconds at 15 fps)
    
    (1) Groups light (CS+/DS+/DS-) and lever presence into intervals of presence 
    (2) Using presence of left and right levers, combines their presence into one "lever presence" interval 
        - uses the first frame of lever presence if a light is illuminated and the last frame of light cue presence (can be for the other lever if the initial lever got hidden before the end of trial interval)
    (3) Creates new intervals of CS+/DS+/DS- presence qualified as "prime" or "trial"
        - prime: from cue onset to lever presence onset
        - trial: from lever presence onset to cue offset
    """
    
    cue_presence = {}
    lever_presence = [] # lever names do not matter
    for object_name, groups in detector_data.items():
        if object_name in cues:
            cue_presence[object_name] = groups
        elif "lever" in object_name:
            lever_presence.extend(groups)
    
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
    
    intervals:list[ dict[str,str|int] ] = []
    for cue, cue_groups in cue_presence.items():
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

def get_countsandduration(grouped_list:list[dict[str,str | int]]) -> dict[str, dict[str,str | int]]:
    """
    Returns: 
        {"behavior name": {"count": int, "duration": int, "latencies": [int, int, ...] }, ... }}
        Where 'Latencies' is a list of the first frame of each behavior occurence
    """
    cd_dict = {}

    for group in grouped_list:
        if not cd_dict.get(group['behavior']):
            cd_dict[group['behavior']] = {"Count":1,"Duration": [group['frame_duration']],"Latencies":[group['first_frame']]}
        else:
            cd_dict[group['behavior']]['Count'] += 1
            cd_dict[group['behavior']]['Duration'].append(group['frame_duration'])
            cd_dict[group['behavior']]['Latencies'].append(group['first_frame'])
    
    for behavior in cd_dict:
        cd_dict[behavior]['Duration'] = avg(cd_dict[behavior]['Duration'])[1] # behavior average durations

    return cd_dict

def add_and_remove_latencies_in_dict(cd_list:dict[str, dict[str, str | int | dict[str,int]]],detection, evoked_behaviors:list[str]):
    """
    updates dictionnary.
    Args:
        cd_list: {"behavior name": {}}
    **Returns None**
    """
    done_latency_behaviors:dict[str, int] = {}
    for behavior, properties in cd_list.items():
        if behavior in evoked_behaviors:
            first_frames:list[int] = properties['Latencies'] # The first frame of each occurence 
            latencies:list[int] = []
            cue = evoked_behaviors[behavior]
            for time in first_frames:
                for trial_number, props in enumerate(detection.get(cue,[])): # assuming each "group" 
                    first:int = props['first_frame']
                    last:int = props['last_frame']
                    if trial_number != done_latency_behaviors.get(behavior): # first encounter with behavior for this trial
                        if first < time < last:
                            latencies.append({"trial":trial_number,"Latency":time - first}) # time to respond in frames (1/15th of a second)
                            done_latency_behaviors[behavior] = trial_number

            properties['Latencies'] = latencies
        else:
            del properties['Latencies'] # no latency if not evoked

def lists_for_export(cd_list:dict,behaviors_in_final_output:list[str]) -> dict[str,list[str | float | int]]:
    clean = {}
    for behavior, properties in cd_list.items():
        if behavior in behaviors_in_final_output: # filter out unwanted behaviors
            if properties.get('Latencies'):
                trials:dict[int,int] = {}
                current_trial:int = None
                max_trial = 0

                for props in properties['Latencies']:
                    if current_trial != props['trial']:
                        trials.update({props['trial']:props['Latency']})
                        current_trial = props['trial']

                    if max_trial < props['trial']: # number of rows needed for latencies
                        max_trial = props['trial']
                # pad with empty strings trials without any occurence of the evoked behavior
                latencies:list[int] = [trials.get(row,'') for row in range(max_trial+1)]
                clean[behavior] = [
                    "Count",
                    properties["Count"],
                    "Duration (s)",
                    properties["Duration"] / 15,
                    "Latencies (s)" 
                ]
                clean[behavior].extend(latencies)
            else:  # non-evoked by cue (ex: grooming)
                clean[behavior] = [
                    "Count",
                    properties["Count"],
                    "Duration",
                    properties["Duration"]
                ]
    return clean

def export_to_excel(input_dict):
    """
    reorganize behavior counts, latencies and durations for each cage into an excel where sheets are behaviors and columns are "Count", "Duration (s)", "Latencies (s)" for each cue
    """
    input_dict = {"date-session name" : #excel filename
                  {"cage 3":{}
                  }}


def main():
    detectorResults_folder = select_folder("Select folder containing detection result folders")
    if not detectorResults_folder:
        return
    analysisResults_folder = select_folder("Select folder containing analysis subfolders each corresponding to a video (ex: all_events.xlsx)")
    if not analysisResults_folder:
        return

    behavior_names = set()
    light_positions = set()

    for video_folder in list_folderspaths(analysisResults_folder):
        for behavior_name in list_folders(video_folder):
            behavior_names.add(behavior_name)
            if "light" in behavior_name:
                light_positions.add(behavior_name.split(" ")[0]) # FL light interaction

    light_positions = list(light_positions)
    light_positions.sort()
    behavior_names = list(behavior_names)
    behavior_names.sort()
    light_position_significance:dict[str,str] = grid_selector(light_positions, ["DS+","DS-","CS+"])
    
    included_behaviors = check(behavior_names)


    


    paired_analysisExcel_detectorExcels, object_names = step0_pair_detectorExcels_analysisExcel(detectorResults_folder, analysisResults_folder)
    for analysisExcel, detectorExcels in paired_analysisExcel_detectorExcels.items():
        detector_data = {}
        for det_excel in detectorExcels:
            if det_excel.endswith(".xlsx"):
                detector_data.update(step1_detector_excel_to_object_times(det_excel))
        
        interval_times = determine_interval_times_from_detector(detector_data)
        # future implementation: use interval times to adjust the analysis Excel data (ex: all_events.xlsx) and export a new Excel sheet with adjusted data (ex: "all_events_adjusted.xlsx")



if __name__ == "__main__":
    main()
 