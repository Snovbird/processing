from common.common import select_anyfile,msgbox,error,list_folders,select_folder
import json, os
import pandas
def excel_to_list(file_path):
    """One-liner version with proper string-to-list conversion"""
    import ast
    try:
        df = pandas.read_excel(file_path, sheet_name=0)
        return [[ast.literal_eval(item)[0] if isinstance(item, str) else item 
                for item in df[col].tolist()] for col in df.columns]
    except Exception as e:
        error(f"Cannot read '{file_path}'. Conversion to list failed: {e}")
        return None

def group_consecutive_elements(lst):
    """
    Group consecutive identical elements and return list of dictionaries with name and count.
    
    Args:
        lst: Input list of elements
    
    Returns:
        List of dictionaries with 'name' and 'count' keys
    """
    if not lst:
        return []
    
    result = []
    current_item = lst[0]
    current_count = 1
    
    for i in range(1, len(lst)):
        if lst[i] == current_item:
            current_count += 1
        else:
            # Add the completed group to result
            result.append({"name": current_item, "frame_duration": current_count})
            # Start new group
            current_item = lst[i]
            current_count = 1
    
    # Don't forget the last group
    result.append({"name": current_item, "frame_duration": current_count})
    
    return result

# def merge_same_names(list_of_dicts):
#     """
#     Group consecutive dictionaries with the same 'name' key and combine their 'frame_duration' values.
#     Non-consecutive dictionaries with the same name will remain separate.
    
#     Args:
#         list_of_dicts: List of dictionaries with 'name' and 'frame_duration' keys
        
#     Returns:
#         List of dictionaries with combined frame_duration for consecutive same names
#     """
#     if not list_of_dicts:
#         return []
    
#     result = []
#     current_name = list_of_dicts[0]["name"]
#     current_frames = list_of_dicts[0]["frame_duration"]
    
#     for i in range(1, len(list_of_dicts)):
#         if list_of_dicts[i]["name"] == current_name:
#             # Same name as previous - combine frame_duration
#             current_frames += list_of_dicts[i]["frame_duration"]
#         else:
#             # Different name - save current group and start new one
#             result.append({"name": current_name, "frame_duration": current_frames})
#             current_name = list_of_dicts[i]["name"]
#             current_frames = list_of_dicts[i]["frame_duration"]
    
#     # Don't forget the last group
#     result.append({"name": current_name, "frame_duration": current_frames})
    
#     return result
# Alternative version that preserves order of first occurrence
def merge_same_names_preserve_order(list_of_dicts,list_of_times):
    """
    Same as above but preserves the order of first occurrence of each name.
    """
    if not list_of_dicts:
        return []
    
    seen = {}
    result = []
    
    for item in list_of_dicts:
        name = item["name"]
        count = item["frame_duration"]

        
        if name in seen:
            # Find and update existing entry
            for existing in result:
                if existing["name"] == name:
                    existing["frame_duration"] += count
                    break
        else:
            # Add new entry
            result.append({"name": name, "frame_duration": count,"first_frame":list_of_times[list_of_dicts.index(item)]})
            seen[name] = True
    
    return result

# def group_consecutive_elements_v2(lst):
#     """More concise version using itertools.groupby"""
#     from itertools import groupby
    
#     return [{"name": key, "frame_duration": len(list(group))} 
#             for key, group in groupby(lst)]


def main():
    while True:
        xlsx_path:str = select_anyfile("Find the excel file containing data", specific_ext="xlsx")[0]
        if not xlsx_path:
            return
        if os.path.basename(xlsx_path) == "all_events.xlsx":
            break
        elif os.path.basename(xlsx_path) == "1_RAT_all_event_probability.xlsx":
            pass # different treatment # future implementation
        else:
            error(f"'{os.path.basename(xlsx_path)}' is not the correct file.\nSelect 'all_events.xlsx' or '1_RAT_all_event_probability.xlsx'")
    video_names = list_folders(os.path.dirname(xlsx_path))
    columns_list = excel_to_list(xlsx_path)
    frame_times = columns_list.pop(0) # remove timestamps column

    count_per_video = {}
    for video_number,column in enumerate(columns_list):
        grouped = group_consecutive_elements(column,frame_times)
        for count in range(len(grouped) - 1, -1, -1): #iterate backwards to use pop
            if grouped[count]["name"] == "NA" and grouped[count]["frame_duration"] < 3:
                grouped.pop(count)
        count_per_video[video_names[video_number]] = grouped
    for key,val in count_per_video.items():
        count_per_video[key] = merge_same_names(val)
    with open(f"{os.path.dirname(xlsx_path)}/all_events_counts.json", "w") as f:
        json.dump(count_per_video, f, indent=2)
    # os.startfile(os.path.dirname(xlsx_path))

def dict_to_excel_advanced(data_dict, output_path=None, filename="ACTUAL behavior counts.xlsx", sheet_name="behavior counts"):
    """
    Advanced version with more formatting options.
    """
    try:
        if not output_path:
            output_path = select_folder("Select folder to save Excel file")
            if not output_path:
                return None
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        full_path = os.path.join(output_path, filename)
        
        # Create Excel writer object for more control
        with pandas.ExcelWriter(full_path, engine='openpyxl') as writer:
            # Create DataFrame
            df = pandas.DataFrame([data_dict])
            
            # Write to Excel
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
            
            # Optional: Access workbook for additional formatting
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Excel file created successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return None

if __name__ == "__main__":
    main()