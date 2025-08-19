from common.common import select_anyfile,msgbox,error,list_folders,select_folder,askint,list_folderspaths,avg,list_files
import json, os
import pandas
from excel.writer_complex import writer_complex 
from excel.general import fit_columns,excel_to_list
from excel.export import export_excel

def detector_excel_to_object_times(excel_path: str) -> dict[str, list[dict[str, int]]]:
    """
    {"Object_name": [
        {"first_frame": ..., "frame_duration": ..., "last_frame": ...},
        ...
        ]}
    """
    detector_data = {}
    try:
        df = pandas.read_excel(excel_path, sheet_name=None)  # Read all sheets
        object_name = os.path.splitext(os.path.basename(excel_path))[0]
        
        for sheet_name, sheet_df in df.items(): # only 1 iteration (sheet1)
            # Assuming the sheet name is the video name NOT TRUE
            # object_name = sheet_name
            
            if 'start_frame' in sheet_df.columns and 'end_frame' in sheet_df.columns:
                events = []
                # Get column B (index 1) values
                column_b_values = sheet_df.iloc[:, 1]  # Second column (index 1)
                
                for idx, value in enumerate(column_b_values):
                    if pandas.notna(value):  # Skip NaN/empty values
                        try:
                            # Assuming column B contains start_frame values
                            start_frame = int(value)
                            # You'll need to define how to get end_frame from column B
                            # Option 1: If column B contains both start and end (e.g., "start-end")
                            # Option 2: If you have a pattern to calculate end_frame
                            end_frame = start_frame + 10  # Example: assuming 10 frame duration
                            
                            events.append({
                                'first_frame': start_frame,
                                'frame_duration': end_frame - start_frame + 1,
                                'last_frame': end_frame
                            })
                        except (ValueError, TypeError):
                            continue  # Skip invalid values
                detector_data[object_name] = events
                
            elif 'first_frame' in sheet_df.columns and 'frame_duration' in sheet_df.columns:
                events = []
                # Get column B (index 1) values
                column_b_values = sheet_df.iloc[:, 1]  # Second column (index 1)
                
                for idx, value in enumerate(column_b_values):
                    if pandas.notna(value):  # Skip NaN/empty values
                        try:
                            # Assuming column B contains first_frame values
                            first_frame = int(value)
                            # You'll need to define how to get frame_duration
                            frame_duration = 10  # Example: default duration
                            
                            events.append({
                                'first_frame': first_frame,
                                'frame_duration': frame_duration,
                                'last_frame': first_frame + frame_duration - 1
                            })
                        except (ValueError, TypeError):
                            continue  # Skip invalid values
                detector_data[object_name] = events
                
            else:
                print(f"Warning: Sheet '{sheet_name}' in '{excel_path}' does not contain expected columns for detector data.")
                detector_data[object_name] = []
    except Exception as e:
        error(f"Error: {e}")

def group_remove_2NA(list_of_behaviors_strings:list[str]):
    """
    Group consecutive identical elements and removes consecutive 2 "NA"
    
    Args:
        list_of_behaviors_strings: Input list of consecutive behavior names
    
    Returns:
        List of dictionaries 
    """
    if not list_of_behaviors_strings:
        return []
    result = []
    current_item:str = list_of_behaviors_strings[0]
    current_count = 1
    
    for i in range(1, len(list_of_behaviors_strings)):
        # 1 more frame if consecutive
        if list_of_behaviors_strings[i] == current_item:
            current_count += 1
        else: # first encounter (beginning) of a set
            result.append({"behavior": current_item, "frame_duration": current_count,"first_frame": i}) # NOTE: first frame is 1 (not 0) 
            # Start new group
            if list_of_behaviors_strings[i] == "NA" and list_of_behaviors_strings[i+2] != 'NA':
                pass # keep same current item
            else:
                current_item = list_of_behaviors_strings[i]
                current_count = 1
    
    # Don't forget the last group
    result.append({"behavior": current_item, "frame_duration": current_count, "first_frame": len(list_of_behaviors_strings) - current_count + 1})
    
    return result

def find_missing_counts(list_of_grouped_behaviors:list[dict[str,str | int]]) -> tuple[list[dict], list[str]]:
    behaviors_missed:dict[str, int] = {}

    cues = set()
    for n, bv_set in enumerate(list_of_grouped_behaviors):
        behavior = bv_set['behavior']
        

        #                   2 possibilities: 
        # 1) Interaction alone (no approach or orient)
        # 2) Interaction with OR before (still no approach)
        if behavior.startswith("Interaction"):

            cue: str = behavior.replace("Interaction", "")
            cues.add(cue)
            
            # Check if we have a previous behavior (n-1 exists)
            if n > 0:
                last = list_of_grouped_behaviors[n-1]['behavior']  
                lastcue = last.replace("Interaction", "").replace("Approach", "").replace("Orient", "")
                cues.add(lastcue)
                if not last.startswith('Approach') or cue != lastcue:  # different cues in case [n-1] was an approach but for a different cue => No approach before interaction "n"
                    approach_behavior_missed = f"Approach{cue} NOT QUANTIFIED"
                    
                    if approach_behavior_missed not in behaviors_missed:
                        behaviors_missed[approach_behavior_missed] = 1
                    else:
                        behaviors_missed[approach_behavior_missed] += 1
                    
                    # Check if we have a behavior two positions ago (n-2 exists)
                    if n > 1:
                        try: 
                            two_ago = list_of_grouped_behaviors[n-2]['behavior']  # n-3 because enumerate starts at 1
                            two_ago_cue = two_ago.replace("Orient", "").replace("Approach", "").replace("Interaction", "")
                            cues.add(two_ago_cue)

                            # If only interaction (no approach nor OR)
                            if not two_ago.startswith('Orient') or two_ago_cue != cue:  # different cues in case [n-2] was an OR but different cue => No OR before approach "n-1"
                                orient_behavior_missed = f"Orient{cue} NOT QUANTIFIED"
                                if orient_behavior_missed not in behaviors_missed:
                                    behaviors_missed[orient_behavior_missed] = 1
                                else:
                                    behaviors_missed[orient_behavior_missed] += 1
                        except IndexError:
                            pass
            else:
                # First behavior is an interaction, so both approach and orient are missing
                approach_behavior_missed = f"Approach{cue} NOT QUANTIFIED"
                orient_behavior_missed = f"Orient{cue} NOT QUANTIFIED"
                behaviors_missed[approach_behavior_missed] = behaviors_missed.get(approach_behavior_missed, 0) + 1 # increment if already exists
                behaviors_missed[orient_behavior_missed] = behaviors_missed.get(orient_behavior_missed, 0) + 1
        
        # If [n] is approach but [n-1] is not orient/orient for different cue
        elif behavior.startswith("Approach"):
            cue = behavior.replace("Approach", "")
            cues.add(cue)
            # Check if we have a previous behavior
            if n > 0:
                last = behaviors_missed[n-1]['behavior']  # n-2 because enumerate starts at 1
                lastcue = last.replace("Approach", "").replace("Orient", "").replace("Interaction", "")
                cues.add(lastcue)
                if not last.startswith('Orient') or cue != lastcue:
                    orient_behavior_missed = f"Orient{cue} NOT QUANTIFIED"
                    if orient_behavior_missed not in behaviors_missed:
                        behaviors_missed[orient_behavior_missed] = 1
                    else:
                        behaviors_missed[orient_behavior_missed] += 1
            else:
                # First behavior is an approach, so orient is missing
                orient_behavior_missed = f"Orient{cue} NOT QUANTIFIED"
                behaviors_missed[orient_behavior_missed] = behaviors_missed.get(orient_behavior_missed, 0) + 1

    return behaviors_missed,cues

def get_countsandduration(grouped_list:list[dict[str,str | int]]) -> dict[str, dict[str,str | int]]:
    cd_dict = {}

    for group in grouped_list:
        if not cd_dict.get(group['behavior']):
            cd_dict[group['behavior']] = {"Count":1,"Duration": [group['frame_duration']],"Latency":[group['first_frame']]}
        else:
            cd_dict[group['behavior']]['Count'] += 1
            cd_dict[group['behavior']]['Duration'].append(group['frame_duration'])
            cd_dict[group['behavior']]['Latency'].append(group['first_frame'])
    
    for behavior in cd_dict:
        cd_dict[behavior]['Duration'] = avg(cd_dict[behavior]['Duration'])[1] # behavior average durations

    return cd_dict

def main():
    while True:
        xlsx_path:str = select_anyfile("Find the excel file containing data", specific_ext="xlsx")[0]
        if not xlsx_path:
            return
        if os.path.basename(xlsx_path) == "all_events.xlsx":
            break
        elif os.path.basename(xlsx_path) == "1_RAT_all_event_probability.xlsx":
            pass # different treatment since data in column 2 ( [1] ) is formatted with strings like "['behavior','probability']" # future implementation
        else:
            error(f"'{os.path.basename(xlsx_path)}' is not the correct file.\nSelect 'all_events.xlsx' or '1_RAT_all_event_probability.xlsx'")

    if os.path.basename(xlsx_path) == "all_events.xlsx":
        
        folder_of_detection = select_folder("Select folder containing detection result folders")
        #minimum_probability = askint("Enter required probability out of 100","Minimum probability")
        video_names:list[str] = list_folders(os.path.dirname(xlsx_path))
        columns_list_with_probabilities:list[ list[str] ] = excel_to_list(xlsx_path)
        frame_times:list[str] = columns_list_with_probabilities.pop(0) # remove timestamps column
        corrected_data: dict[str, dict [str, list[dict[str,str | int]]]] = {}
        # list_of_columns = [[behavior if float(probability) >= minimum_probability else "NA" 
        #              for behavior, probability in video_column] for video_column in columns_list_with_probabilities]
        columns_list = [i[0] for i in columns_list_with_probabilities]
        


        for video_name, column in zip(video_names, columns_list):
            
            grouped:list[dict[str,str | int]] = group_remove_2NA(column)

            NO_NA_list = [group for group in grouped if group['behavior'] != "NA"]
            
            cd_list = get_countsandduration(NO_NA_list)

            missing_counts, cues = find_missing_counts(NO_NA_list)

            detection_excels = os.path.join(folder_of_detection,video_name)

            detection = {} 
            for excel in list_files(detection_excels):
                
                if excel.startswith("light") and excel.endswith(".xlsx"):
                    for cue in cues:
                        if cue in excel: # usually DS+ or DS-. CS+ might be next
                            detection.update(detector_excel_to_object_times(os.path.join(detection_excels,excel)))
            
            for object in detection:
                

            
            
 



main()