from common.common import select_anyfile,msgbox,error,list_folders,select_folder
import json, os
import pandas
    
def excel_to_list(file_path:str) -> list[list[int | str]]:
    """One-liner version with proper string-to-list conversion"""
    import ast
    try:
        df = pandas.read_excel(file_path, sheet_name=0)
        return [[ast.literal_eval(item)[0] if isinstance(item, str) else item 
                for item in df[col].tolist()] for col in df.columns]
    except Exception as e:
        error(f"Cannot read '{file_path}'. Conversion to list failed: {e}")
        return None

def group_consecutive_elements(list_of_behaviors_strings:list[str],list_of_times:list[int]):
    """
    Group consecutive identical elements and return list of dictionaries with name and count.
    
    Args:
        list_of_behaviors_strings: Input list of elements
    
    Returns:
        List of dictionaries with 'name' and 'count' keys
    """
    if not list_of_behaviors_strings:
        return []
    elif len(list_of_behaviors_strings) != len(list_of_times):
        error(f"Lists do not have the same len\n\n Len behaviors = {len(list_of_behaviors_strings)}\nLen timestamps = {len(list_of_times)}\n\n{list_of_behaviors_strings=}\n{list_of_times=}")
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
    
    video_names:list[str] = list_folders(os.path.dirname(xlsx_path))
    columns_list:list[ list[str] ] = excel_to_list(xlsx_path)
    frame_times:list[str] = columns_list.pop(0) # remove timestamps column

    count_per_video:dict[ str , list[ dict[ str, str | int ] ] ] = {}
    for video_number,column in enumerate(columns_list):
        grouped = group_consecutive_elements(column,frame_times)
        for count in range(len(grouped) - 1, -1, -1): #iterate backwards to use pop
            if grouped[count]["behavior"] == "NA" and grouped[count]["frame_duration"] < 3:
                grouped.pop(count)
        count_per_video[video_names[video_number]] = grouped
    for key,val in count_per_video.items():
        count_per_video[key] = merge_same_names_preserve_order(val)
    # with open(f"{os.path.dirname(xlsx_path)}/all_events_counts.json", "w") as f:
    #     json.dump(count_per_video, f, indent=2)
    dict_to_excel_advanced_transposed(data_dict=count_per_video,output_path=os.path.dirname(xlsx_path))
    os.startfile(os.path.dirname(xlsx_path))


if __name__ == "__main__":
    main()