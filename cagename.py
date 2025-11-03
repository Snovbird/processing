import os
import wx
from common.common import select_folder,windowpath,msgbox,list_files

def name_cages(source_folder):
    """Create subfolder and copy files with modified names"""    
    # Get all files in source folder
    files = list_files(source_folder)

    if not files:
        raise Exception("The selected folder does not contain any files.")
    # Copy files with appended names
    
    for filename in files:
        # Create new filename with appended string
        name, extension = os.path.splitext(filename)
        if filename == "desktop.ini":
            continue # skips to next iteration. desktop.ini shows up when you change a folder's appearance
        if '_' not in name :
            print(f"No underscore in {name}. Skipping")
            continue
        thedate = name.split('_')[3][:8] # to get YYYYMMDD
        # N864A6_ch1_main_20250714103626_20250714110000
        start_time = name.split('_')[3][8:] # to get HHMMSS
        end_time = name.split('_')[4][8:] # to get HHMMSS
        cage_number = name.split('_')[1].replace('ch','')
        # letter_ord_value = 97 # "a"
        full_renamed_path = os.path.join(source_folder,f"{cage_number}-{thedate}-{start_time}-{end_time}{extension}")
        # while os.path.exists(full_renamed_path) and letter_ord_value < 123:
        #     letter_ord_value += 1
        #     full_renamed_path = os.path.join(source_folder,f"{cage_number}-{thedate}-{start_time}-{end_time}{extension}")
        os.rename(os.path.join(source_folder,filename),full_renamed_path)
            
    

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
