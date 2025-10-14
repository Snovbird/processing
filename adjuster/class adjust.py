import json, os, pandas
from dependencies import *

class AdjustData: 
    def __init__(self, analysis_data_path: str=None,detector_data_dir: str=None):
        if not analysis_data_path:
            self.analysis_data_path = self.get_analysis_data()
        else:
            self.analysis_data_path = analysis_data_path # default: None | excel file path for categorized behaviors for 1 or more videos
        if not detector_data_dir:
            self.detector_data_dir = self.get_detector_xlsx()
        else:
            self.detector_data_dir = detector_data_dir # default: None | folder path containing subfolders each containing detection data for 1 or more videos
        self.analysis_data = {}
        self.detector_files = {}
        self.behaviors_of_interest = [] # behaviors selected by the user. Included in output.
        self.cues_in_detector = set() # Cage objects the rat can orient to such as: FNCL, FFCL, BNCL, BFCL
        self.cues_of_interest = [] # Cues 
        self.detector_data = {}
        self.corrected_data:dict[str, dict[str,list[str|int]]] = {} # excel ready to be written to a file

    def get_analysis_data(self) -> list[list[ list[str|float] ]]:
        '''
        file explorer for analysis data
        '''
        msgbox("Select the excel file named 'all_events.xlsx' containing the analysis data")
        while not self.analysis_data_path: # find right excel sheet
            self.analysis_data_path:str = file_explorer("Find the excel file containing analysis data", xlsx_only=True)[0]

            if not os.path.basename(self.analysis_data_path) == "all_events.xlsx":
                error(f"'{os.path.basename(self.analysis_data_path)}' is not the correct file.\nSelect 'all_events.xlsx'")
        
        return self.analysis_data_path
                
    def get_detector_xlsx(self): 
        '''
        **Folder** explorer for detection data
        '''
        while not self.detector_data_dir: # start explorer again if wrong excel seleted
            self.detector_data_dir:str = folder_explorer("Find the parent directory containing detection data folders")
            
            if list_files(self.detector_data_dir): # picked the "wrong" folder inside (should be otherwise None)

                if 'Analysis log.txt' in list_files(self.detector_data_dir): 
                    self.detector_data_dir = os.path.dirname(self.detector_data_dir)
                else:
                    error("Please select a repository that contains detection data FOLDERS")
        
        self.detector_files:dict[str, list[str]] =  {video_name:[file for file in list_filespaths(dirpath) if file.endswith("_all_centers.xlsx")] for dirpath, video_name in zip(list_folderspaths(self.detector_data_dir),list_folders(self.detector_data_dir))}
        
        return self.detector_files

    def get_cues(self):
        if not self.detector_files:
            self.get_detector_xlsx()
            
        for group in self.detector_files.values():
            for xlsx in group:
                self.cues_in_detector.add(os.path.basename(xlsx).replace("_all_centers.xlsx",""))
        self.cues_in_detector.remove("1-Rat")
        self.cues_of_interest = checkbox_dialog(self.cues_in_detector,"Select cues that evoke behaviors, for which latencies will be extracted:","Cues of interest")              
        
        return self.cues_of_interest
    
    def process_detector_data(self,minimum_detection_frames=10,minimum_blank_frames=0):
        '''
        Inputs**:**
            cues_of_interest: list of objects in the cage that will evoke behaviors. These behaviors will have latencies
            minimum_detection_frames: minimum duration in frames 

        Args:
            minimum_detection_frames: minimum duration in frames for a detection group to be considered valid, 
            minimum_blank_frames: minimum duration in frames of a blank space to separate two detection groups
            if 0, blank space of any length will separate two detection groups

        '''
        if not self.cues_of_interest:
            self.get_cues()

        for video, xlsx_files in self.detector_files.items():
            self.detector_data[video] = {}
            
            for xlsx in xlsx_files: # full paths
                object_name = os.path.basename(xlsx).replace("_all_centers.xlsx","")
                if object_name.replace("_all_centers.xlsx","") in self.cues_of_interest: # check if cue is of interest, else behaviors evoked by this will not have latencies
                    object_name = os.path.basename(xlsx).replace("_all_centers.xlsx","")
                    self.detector_data[video][object_name] = []
                    objdata:list[dict[str,int,bool]] = self.detector_data[video][object_name]

                    object_detected = False
                    
                    load_col2:pandas.DataFrame = pandas.read_excel(xlsx, usecols=[1]) # only load second column
                    column_name = load_col2.columns[0]  # Get the actual column name
                    col2_data:list[str] = load_col2[column_name]

                    for row, value in enumerate(col2_data, start=1):
                        print(f"Row {row}: {value}")
                        if pandas.notna(value): # blank
                            if object_detected:
                                object_detected = False
                                if objdata[-1]['detection duration'] < minimum_detection_frames: # convert unsufficient detected group to blank
                                    duration_to_add = objdata[-1]['detection duration']
                                    del objdata[-1]
                                else:
                                    objdata[-1]["last frame": row-1] # last frame of detection group
                                    objdata.append({"obj": False, "blank duration": 1})
                            elif row == 1:
                                objdata.append({"obj": False, "blank duration": 1})
                            else:
                                objdata[-1]["blank duration"] +=1
                        else:
                            if not object_detected:
                                object_detected = True
                                # if objdata[-1]['blank duration'] < minimum_blank_frames: # add the blank duration to an active detection group
                                #     # issue: what if there is just a brief detection of an object (False positive ex: BNCL) → blanks should have priority
                                #     duration_to_add = objdata[-1]['blank duration']
                                #     del objdata[-1]
                                #     objdata[-1]['detection duration'] += duration_to_add
                                if row == 1:
                                    objdata.append({"obj": True, "detection duration": 1,"first frame": row})
                                else:
                                    objdata.append({"obj": True, "detection duration": 1,"first frame": row})                                
                            else:
                                objdata[-1]["detection duration"] +=1
        return self.detector_data

    def process_analysis_data(self): # please make sure that columns are video file names in alphabetical order
        import ast
        df = pandas.read_excel(self.analysis_data_path, sheet_name=0)
        # Each column is made of behavior names and its probability for each frame for one video (except first col). ex: "['behavior_name',0.842304238]"
        lambda column
        self.analysis_data:list[list[ list[str|float] ]] = [ [ast.literal_eval(item) if isinstance(item, str) else item for item in df[col].tolist()] for col in df.columns]
        # list:videos [ list:cell data [ str:behavior name, float:probability ] ]
        
        

if __name__ == "__main__":
    result = AdjustData(detector_data_dir=r"C:\Users\matts\Downloads\detector").process_detector_data(minimum_detection_frames=2,minimum_blank_frames=0)

    print(result)
    msgbox(result)

        
if False:
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
            
            for sheet_df in df.values():
                events = []
                
                # Get column B (index 1) values
                column_b_values = sheet_df.iloc[:, 1]  # Second column (index 1)
                
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
                    else:  # Blank value or NaN
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
            error(f"Error processing detector Excel file '{excel_path}': {e}")
            return {}
        
        return detector_data

    def group_remove_2NA(list_of_behaviors_strings:list[str]):
        """
        Group consecutive identical elements and removes consecutive 2 "NA"

        [
        {"behavior": "name", "frame_duration": int, "first_frame": int}, ...
        ]
        
        
        Args:
            list_of_behaviors_strings: Input list of consecutive behavior names

        
        Returns:
            List of dictionaries 
        """
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

    def find_missing_counts(list_of_grouped_behaviors: list[dict[str, str | int]]) -> tuple[dict[str, list[str, int]], set[str]]:
        behaviors_missed: dict[str, list[str, int]] = {}
        cues = set()
        
        for n, bv_set in enumerate(list_of_grouped_behaviors):
            behavior = bv_set['behavior']
            
            # Extract cue from any behavior type
            for behavior_type in ["Interaction", "Approach", "Orient"]:
                if behavior.startswith(behavior_type):
                    cue = behavior.replace(behavior_type, "")
                    cues.add(cue)
                    break
            else:
                continue  # Skip if behavior doesn't match any type
            
            # Process Interaction behaviors
            if behavior.startswith("Interaction"):
                missing_behaviors = []
                
                # Check for missing Approach
                if n > 0:
                    last_behavior = list_of_grouped_behaviors[n-1]['behavior']
                    last_cue = last_behavior.replace("Interaction", "").replace("Approach", "").replace("Orient", "")
                    
                    if not last_behavior.startswith('Approach') or cue != last_cue:
                        missing_behaviors.append(f"Approach{cue} NOT QUANTIFIED")
                        
                        # Check for missing Orient (two positions ago)
                        if n > 1:
                            two_ago_behavior = list_of_grouped_behaviors[n-2]['behavior']
                            two_ago_cue = two_ago_behavior.replace("Orient", "").replace("Approach", "").replace("Interaction", "")
                            
                            if not two_ago_behavior.startswith('Orient') or two_ago_cue != cue:
                                missing_behaviors.append(f"Orient{cue} NOT QUANTIFIED")
                else:
                    # First behavior is interaction - both approach and orient are missing since no cues BEFORE
                    missing_behaviors.extend([f"Approach{cue} NOT QUANTIFIED", f"Orient{cue} NOT QUANTIFIED"])
                
                # Add missing behaviors to the count
                for missing_behavior in missing_behaviors:
                    if missing_behavior not in behaviors_missed:
                        behaviors_missed[missing_behavior] = ["Count", 1]
                    else:
                        behaviors_missed[missing_behavior][1] += 1
            
            # Process Approach behaviors
            elif behavior.startswith("Approach"):
                if n > 0:
                    last_behavior = list_of_grouped_behaviors[n-1]['behavior']
                    last_cue = last_behavior.replace("Approach", "").replace("Orient", "").replace("Interaction", "")
                    
                    if not last_behavior.startswith('Orient') or cue != last_cue:
                        missing_behavior = f"Orient{cue} NOT QUANTIFIED"
                        if missing_behavior not in behaviors_missed:
                            behaviors_missed[missing_behavior] = ["Count", 1]
                        else:
                            behaviors_missed[missing_behavior][1] += 1
                else:
                    # First behavior is approach - orient is missing
                    missing_behavior = f"Orient{cue} NOT QUANTIFIED"
                    if missing_behavior not in behaviors_missed:
                        behaviors_missed[missing_behavior] = ["Count", 1]
                    else:
                        behaviors_missed[missing_behavior][1] += 1

        return behaviors_missed, cues

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

    def export_excel(data:dict[str , dict[str,list[str|int]]],xlsx_path:str="output.xlsx"):
        """
        Args:
        data: {"Sheet Name": {"Column Name": [ data, data] } }.
        xlsx_path: Full or relative path ending by `.xlsx`
        You can also alternate "str" title and int data to have data in same column
        """
        with pandas.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            
            for sheet_name, columns_data in data.items():

                columns_data:dict[str, list[str|int]]

                dataframe = pandas.DataFrame(columns_data)

                dataframe.to_excel(writer, sheet_name=sheet_name, index=False,header=True)

                fit_columns(writer.sheets[sheet_name])
        
        return xlsx_path

    if __name__ == "__main__":

        test_data = {f"Sheet {i}": {f"column {i}":[i for i in range(10)] for i in range(6)} for i in range (3)}

        os.startfile(
            writer_complex(test_data)
            )        

    def main():

        if os.path.basename(xlsx_path) == "all_events.xlsx":
            
            video_names = list_folders(os.path.dirname(xlsx_path))
            folder_of_detection = select_folder("Select folder containing detection result folders")

            if not folder_of_detection:
                return 
            #minimum_probability = askint("Enter required probability out of 100","Minimum probability")
            columns_list_with_probabilities:list[ list[str, int] ] = excel_to_list(xlsx_path)
            columns_list_with_probabilities.pop(0) # remove timestamps column
            # list_of_columns = [[behavior if float(probability) >= minimum_probability else "NA" 
            #              for behavior, probability in video_column] for video_column in columns_list_with_probabilities]
            columns_list: list[str] = [[behavior_and_prob[0] for behavior_and_prob in col] for col in columns_list_with_probabilities] # only behaviors, remove probabilities
            behaviors:list[str] = list_folders(list_folderspaths(os.path.dirname(xlsx_path))[0])
            behaviors_in_final_output = check(behaviors,"Select behaviors to obtain count, duration and latencies (if evoked by cue presence)","Behaviors of interest")
            corrected_data: dict[str, dict [str, list[dict[str,str | int]]]] = {}

            for video_name, column in zip(video_names,columns_list):
                
                grouped:list[dict[str,str | int]] = group_remove_2NA(column)

                NO_NA_list = [group for group in grouped if group['behavior'] != "NA"]
                
                cd_list:dict[str, dict[str, str | int] ] = get_countsandduration(NO_NA_list)
                missing_counts, cues = find_missing_counts(NO_NA_list)
                cues = list(map(letter,cues)) # remove spaces from cue names

                detection_excels = os.path.join(folder_of_detection,video_name)
                detection:dict[str, list[dict[str,int]]] = {} 
                for det_excel in list_files(detection_excels):

                    if det_excel.endswith(".xlsx") and det_excel.split("_")[0] in cues: # is the name "FNCL_all_centers.xlsx" for example
                        detection.update(detector_excel_to_object_times(os.path.join(detection_excels,det_excel)))
                
                evoked_behaviors = {properties['behavior']: properties['behavior'].split()[-1] for properties in NO_NA_list if properties['behavior'].split()[-1] in cues}
                # add latencies using 

                add_and_remove_latencies_in_dict(cd_list,detection,evoked_behaviors)

                corrected_data[video_name] = lists_for_export(cd_list,behaviors_in_final_output)
                corrected_data[video_name].update(missing_counts)
            
            final = {}
            # Before calling writer_complex, normalize all list lengths using empty strings (different lengths = error)
            for video_name in corrected_data:
                max_length = max(len(behavior_list) for behavior_list in corrected_data[video_name].values()) # a generator object IS an iterable (for max fct)
                first_col = {'': ['' if i <= 4 else f"Trial {i -5 +1}:" for i in range(max_length)]}
                final[video_name] = {}
                final[video_name].update(first_col)
                
                for behavior_name in corrected_data[video_name]:
                    current_list = corrected_data[video_name][behavior_name]
                    while len(current_list) < max_length:
                        current_list.append("")  # Pad with empty strings
                final[video_name].update(corrected_data[video_name])

        outpath = os.path.join(os.path.dirname(xlsx_path),"CORRECTED DATA.xlsx")
        c = 1
        while path_exists(outpath):
            c+= 1
            outpath = os.path.join(os.path.dirname(xlsx_path),f"CORRECTED DATA-{c}.xlsx")

        writer_complex(final,outpath)

        os.startfile(os.path.dirname(xlsx_path))

    if __name__ == "__main__":
        main()

    def writer_complex(data:dict[str , dict[str,list[str|int]]],xlsx_path:str="output.xlsx"):
        """
        Args:
        data: {"Sheet Name": {"Column Name": [ data, data] } }.
        xlsx_path: Full or relative path ending by `.xlsx`
        You can also alternate "str" title and int data to have data in same column
        """
        with pandas.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
            
            for sheet_name, columns_data in data.items():

                columns_data:dict[str, list[str|int]]

                dataframe = pandas.DataFrame(columns_data)

                dataframe.to_excel(writer, sheet_name=sheet_name, index=False,header=True)

                fit_columns(writer.sheets[sheet_name])
        
        return xlsx_path

    