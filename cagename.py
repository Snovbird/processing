import os
import wx
from common.common import select_folder,windowpath,msgbox,list_files,custom_dialog

def name_cages(source_folder):
    files = list_files(source_folder)
    
    for filename in files:
        try:
            name, extension = os.path.splitext(filename)
            if filename == "desktop.ini" or '_' not in name:
                continue
                
            parts = name.split('_')
            # print(f"Processing: {filename}")
            # print(f"Parts: {parts}")
            # print(f"Number of parts: {len(parts)}")
            
            if len(parts) < 5:  # Need at least 5 parts
                print(f"Skipping {filename} - insufficient parts")
                continue
                
            cage_number = (
                parts[1].replace('ch','')
            ).zfill(2)
            thedate = parts[3][:8]
            start_time = parts[3][8:]
            end_time = parts[4][8:]
            
            print(f"Cage: {cage_number}, Date: {thedate}, Start: {start_time}, End: {end_time}")
            
            full_renamed_path = os.path.join(source_folder, f"{cage_number}-{thedate}-{start_time}-{end_time}{extension}")
            if os.path.exists(full_renamed_path):
                if custom_dialog(f"ERROR: {os.path.basename(full_renamed_path)} already exists. Overwrite?") == "no":
                    continue
                else:
                    os.remove(full_renamed_path)
            os.rename(os.path.join(source_folder, filename), full_renamed_path)
            # print(f"Successfully renamed to: {os.path.basename(full_renamed_path)}")
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
                

def main():
    # Initialize wx application
    app = wx.App(False)
    
    # Step 1: Ask for folder directory
    source_folder = windowpath()
    if not os.path.isdir(source_folder): # is it a file explorer window and is the setting to show full path in window name active (if not → else)
        source_folder = select_folder()
    if not source_folder:
        return
    # Step 3: Process files
    try:
        name_cages(source_folder)
    except Exception as e:
        pass
    os.startfile(source_folder)


if __name__ == "__main__":
    main()
