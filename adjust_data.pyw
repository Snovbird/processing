from common.common import select_anyfile,msgbox,error,list_folders,select_folder,askint,list_folderspaths,avg,list_files
import json, os
import pandas
from excel.writer_complex import writer_complex 
from excel.general import fit_columns

def excel_to_list(file_path:str) -> list[list[int | str]]:
    """One-liner version with proper string-to-list conversion"""
    import ast
    try:
        df = pandas.read_excel(file_path, sheet_name=0)
        return [[ast.literal_eval(item) if isinstance(item, str) else item # index 0 = behavior name. Index 1 = probability
                for item in df[col].tolist()] for col in df.columns]
    except Exception as e:
        error(f"Cannot read '{file_path}'. Conversion to list failed: {e}")
        return None

def group_consecutive_elements(list_of_behaviors_strings:list[str]):
    """
    Group consecutive identical elements and return list of dictionaries with name and count.
    
    Args:
        list_of_behaviors_strings: Input list of elements
    
    Returns:
        List of dictionaries ]: 
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
            current_item = list_of_behaviors_strings[i]
            current_count = 1
    
    # Don't forget the last group - UNCOMMENT THIS LINE!
    result.append({"behavior": current_item, "frame_duration": current_count, "first_frame": len(list_of_behaviors_strings) - current_count + 1})
    
    return result
# Alternative version that preserves order of first occurrence
def merge_same_names_preserve_order(list_of_dicts: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    """
    Combine only consecutive dictionaries with the same 'behavior' key.
    Non-consecutive behaviors with the same name will remain separate.
    
    Args:
        list_of_dicts: List of dictionaries with 'behavior', 'frame_duration', and 'first_frame' keys
    
    Returns:
        List of dictionaries with combined frame_duration for consecutive same behaviors
    """
    if not list_of_dicts:
        return []
    
    result = []
    current_behavior = list_of_dicts[0]["behavior"]
    current_duration = list_of_dicts[0]["frame_duration"]
    current_first_frame = list_of_dicts[0]["first_frame"]
    
    for i in range(1, len(list_of_dicts)):
        if list_of_dicts[i]["behavior"] == current_behavior:
            # Same behavior as previous - combine durations
            current_duration += list_of_dicts[i]["frame_duration"]
        else:
            # Different behavior - save current group and start new one
            result.append({
                "behavior": current_behavior,
                "frame_duration": current_duration,
                "first_frame": current_first_frame
            })
            # Start new group
            current_behavior = list_of_dicts[i]["behavior"]
            current_duration = list_of_dicts[i]["frame_duration"]
            current_first_frame = list_of_dicts[i]["first_frame"]
    
    # Don't forget the last group
    result.append({
        "behavior": current_behavior,
        "frame_duration": current_duration,
        "first_frame": current_first_frame
    })
    
    return result
# def group_consecutive_elements_v2(lst):
#     """More concise version using itertools.groupby"""
#     from itertools import groupby
    
#     return [{"behavior": key, "frame_duration": len(list(group))} 
#             for key, group in groupby(lst)]

def dict_to_excel_advanced_transposed(data_dict: dict[str, list[dict[str, str | int]]], output_path=None, filename="CORRECTED behavior data.xlsx"):
    """
    Create Excel file with separate sheets for each video.
    Each behavior becomes a column, with behavior names as column headers.
    """
    try:
        if not output_path:
            output_path = select_folder("Select folder to save Excel file")
            if not output_path:
                return None
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        full_path = os.path.join(output_path, filename)
        
        with pandas.ExcelWriter(full_path, engine='openpyxl') as writer:
            
            for video_name, behavior_list in data_dict.items():
                if not behavior_list:
                    continue
                
                # Create a DataFrame where each row represents one behavior instance
                df = pandas.DataFrame(behavior_list)
                
                # Clean sheet name
                clean_sheet_name = str(video_name).replace('/', '_').replace('\\', '_')[:31]
                
                # Write to Excel
                df.to_excel(writer, sheet_name=clean_sheet_name, index=False, header=True) 
                
                # Format the sheet
                workbook = writer.book
                worksheet = writer.sheets[clean_sheet_name]
                
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Excel file created successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return None

def main():

    # make sure the excel is either behaviors over time for multiple videos or for a single video 
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
    
    minimum_probability = askint("Enter required probability out of 100","Minimum probability")

    video_names:list[str] = list_folders(os.path.dirname(xlsx_path))
    raw_columns_list:list[ list[str] ] = excel_to_list(xlsx_path)
    frame_times:list[str] = raw_columns_list.pop(0) # remove timestamps column

    # Replace invalid probabilities by "NA"
    columns_list = [[behavior if float(probability) >= minimum_probability else "NA" 
                     for behavior, probability in video_column] for video_column in raw_columns_list]
    
    corrected_ordered_sets:dict[ str , list[ dict[ str, str | int ] ] ] = {}
    for video_number,column in enumerate(columns_list):
        grouped = group_consecutive_elements(column)
        for count in range(len(grouped) - 1, -1, -1): #iterate backwards to use pop
            if grouped[count]["behavior"] == "NA" and grouped[count]["frame_duration"] < 3:
                grouped.pop(count)
        corrected_ordered_sets[video_names[video_number]] = grouped
    
    behaviors_names = {}
    # group sets that where separated by one or two "NA" frames, then remove all remaining "NA" sets
    for key,val in corrected_ordered_sets.items(): # key = video name, val = list of dicts where each dict = a set of a behavior
        new_column = merge_same_names_preserve_order(val)
        for count in range(len(new_column) - 1, -1, -1): #iterate backwards to use pop
            bv = new_column[count]["behavior"]
            if bv == "NA":# remove "NA" sets
                new_column.pop(count)
            else:
                if not behaviors_names.get(key):
                    behaviors_names[key] = {bv}
                else:
                    behaviors_names[key].add(bv)
        corrected_ordered_sets[key] = new_column
    
    # with open(f"{os.path.dirname(xlsx_path)}/all_events_counts.json", "w") as f:
    #     json.dump(corrected_ordered_sets, f, indent=2)

    new_corrected_ordered_sets = {vid: [item for item in corrected_set
        if item["behavior"] != "NA"] for vid,corrected_set in corrected_ordered_sets.items()
    }

    behaviors_not_quantified:dict[str, dict[str, int]] = {}
    for video_name, behavior_list in new_corrected_ordered_sets.items():

        behaviors_not_quantified[video_name] = {}

        for n, bv_set in enumerate(behavior_list, start=1):
            behavior = bv_set["behavior"]
            
            #                   2 possibilities: 
            # 1) Interaction alone (no approach or orient)
            # 2) Interaction with OR before (still no approach)
            if behavior.startswith("Interaction"):

                cue: str = behavior.replace("Interaction", "")
                
                # Check if we have a previous behavior (n-1 exists)
                if n > 1:
                    last = new_corrected_ordered_sets[video_name][n-2]["behavior"]  # n-2 because enumerate starts at 1
                    lastcue = last.replace("Interaction", "").replace("Approach", "").replace("Orient", "")
                    
                    if not last.startswith('Approach') or cue != lastcue:  # different cues in case [n-1] was an approach but for a different cue => No approach before interaction "n"
                        approach_key = f"Approach{cue} NOT QUANTIFIED"
                        
                        if approach_key not in behaviors_not_quantified[video_name]:
                            behaviors_not_quantified[video_name][approach_key] = 1
                        else:
                            behaviors_not_quantified[video_name][approach_key] += 1
                        
                        # Check if we have a behavior two positions ago (n-2 exists)
                        if n > 2:
                            try: 
                                two_ago = new_corrected_ordered_sets[video_name][n-3]["behavior"]  # n-3 because enumerate starts at 1
                                two_ago_cue = two_ago.replace("Orient", "").replace("Approach", "").replace("Interaction", "")

                                # If only interaction (no approach nor OR)
                                if not two_ago.startswith('Orient') or two_ago_cue != cue:  # different cues in case [n-2] was an OR but different cue => No OR before approach "n-1"
                                    orient_key = f"Orient{cue} NOT QUANTIFIED"
                                    if orient_key not in behaviors_not_quantified[video_name]:
                                        behaviors_not_quantified[video_name][orient_key] = 1
                                    else:
                                        behaviors_not_quantified[video_name][orient_key] += 1
                            except IndexError:
                                pass
                else:
                    # First behavior is an interaction, so both approach and orient are missing
                    approach_key = f"Approach{cue} NOT QUANTIFIED"
                    orient_key = f"Orient{cue} NOT QUANTIFIED"
                    behaviors_not_quantified[video_name][approach_key] = behaviors_not_quantified[video_name].get(approach_key, 0) + 1 # increment if already exists
                    behaviors_not_quantified[video_name][orient_key] = behaviors_not_quantified[video_name].get(orient_key, 0) + 1

            # If [n] is approach but [n-1] is not orient/orient for different cue
            elif behavior.startswith("Approach"):
                cue = behavior.replace("Approach", "")
                
                # Check if we have a previous behavior
                if n > 1:
                    last = new_corrected_ordered_sets[video_name][n-2]["behavior"]  # n-2 because enumerate starts at 1
                    lastcue = last.replace("Approach", "").replace("Orient", "").replace("Interaction", "")
                    
                    if not last.startswith('Orient') or cue != lastcue:
                        orient_key = f"Orient{cue} NOT QUANTIFIED"
                        if orient_key not in behaviors_not_quantified[video_name]:
                            behaviors_not_quantified[video_name][orient_key] = 1
                        else:
                            behaviors_not_quantified[video_name][orient_key] += 1
                else:
                    # First behavior is an approach, so orient is missing
                    orient_key = f"Orient{cue} NOT QUANTIFIED"
                    behaviors_not_quantified[video_name][orient_key] = behaviors_not_quantified[video_name].get(orient_key, 0) + 1
    # Process detector excel
    # path_to_detection
    # for list_files in list_files(os.path.dirname()):



    # If we want empty data 
    # all_behaviors_names = list_folders(list_folderspaths(os.path.dirname(xlsx_path))[0])
    # cues:set = {name.replace("Interaction",'') for name in all_behaviors_names if name.startswith("Interaction")}
    # evoked_behaviors = []
    # for cue in cues:
    #     evoked_behaviors.append([f"Orient{cue}",f"Approach{cue}",f"Interaction{cue}"])
    # columns:dict[str,list[str]] = { cue : {bv : {"Count":0,"Duration":[],"Latency":0,"Latency for each occurence":[]} for bv in evoked_behaviors[n]} for n, cue in enumerate(evoked_behaviors) 
    # }

    # { "vid": {}}
    dict_counts_duration:dict[str, dict[ str, list[ dict[ str, str | int ]  ] ]] = {}
    for video_name, behavior_list_of_sets in new_corrected_ordered_sets.items():
        dict_counts_duration[video_name] = {}
        for behavior_set in behavior_list_of_sets:
            if not dict_counts_duration.get(behavior_set["behavior"]):
                dict_counts_duration[video_name][behavior_set["behavior"]] = {"Count":1,"Duration":[behavior_set["frame_duration"]],"Latency":[behavior_set["first_frame"]],"Latency for each occurence":[]}
            else:
                dict_counts_duration[video_name][behavior_set["behavior"]]["Count"] += 1
                dict_counts_duration[video_name][behavior_set["behavior"]]["Duration"].append(behavior_set["frame_duration"])
                dict_counts_duration[video_name][behavior_set["behavior"]]["Latency"].append(behavior_set["first_frame"])
        
    for video_name in dict_counts_duration:
        for behavior in dict_counts_duration[video_name]:
            dict_counts_duration[video_name][behavior]["Duration"] = avg(dict_counts_duration[video_name][behavior]["Duration"])[1]

    final = {}

    for video_name in dict_counts_duration:
        final[video_name] = {}
        for behavior in dict_counts_duration[video_name]:
            final[video_name][behavior] = [
                "Count",
                dict_counts_duration[video_name][behavior]["Count"],
                "Duration", 
                dict_counts_duration[video_name][behavior]["Duration"],  # Convert fraction to float
                "Latency",
                dict_counts_duration[video_name][behavior]["Latency"]
            ]    
        # with open(f"{os.path.dirname(xlsx_path)}/all_events_counts.json", "w") as f:
        #     json.dump(final, f, indent=2)

            # for n, latency in enumerate(dict_counts_duration[video_name]["Latency"]):
            #     for start_DSplus, end_DSplus in [(times['first_frame'], times['first_frame'] + times['frame_duration'] for times in detection_sets]
            #         if start_DSplus < latency < end_DSplus:
    # msgbox(f"{}")
    for video in dict_counts_duration:        
        # Iterate over items in behaviors_not_quantified[video]
        for behavior, count in behaviors_not_quantified[video].items():
            # Ensure the behavior key exists in final[video] before appending
            if behavior not in final[video]:
                final[video][behavior] = ["Count", count]
            else:
                # If behavior already exists, just update the count
                final[video][behavior][1] = count  # Assuming Count is always first
    # msgbox(f"{final}")

    # Before calling writer_complex, normalize all list lengths using empty strings (different lengths = error)
    for video_name in final:
        max_length = max(len(behavior_list) for behavior_list in final[video_name].values()) # a generator object IS an iterable (for max fct)
        for behavior_name in final[video_name]:
            current_list = final[video_name][behavior_name]
            while len(current_list) < max_length:
                current_list.append("")  # Pad with empty strings

    

    writer_complex(data=final,xlsx_path=os.path.join(os.path.dirname(xlsx_path),"all_events_counts.xlsx"))
    # dict_to_excel_advanced_transposed(data_dict=new_corrected_ordered_sets,output_path=os.path.dirname(xlsx_path))
    os.startfile(os.path.dirname(xlsx_path))


if __name__ == "__main__":
    main()