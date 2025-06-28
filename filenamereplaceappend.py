import os
import shutil
import wx
from common.common import windowpath,select_folder,custom_dialog,askstring,msgbox,error
def main():
    # Initialize wx application
    # app = wx.App(False)
    
    # Step 1: Ask for folder directory
    source_folder = windowpath()
    if not os.path.isdir(source_folder):
        source_folder = select_folder()
    if not source_folder:
        return
    
    # Step 2: Ask for string input
    toreplace = askstring("Enter String to REPLACE", 'Str remover')
    append_string = askstring("Enter string to append to filenames:","String Input")
    if append_string:
        START_or_END = custom_dialog('Place string at the START or END of the file name?','START or END','START',"END")

    if not append_string:
        append_string = ''
        START_or_END = 'END'
    
    # Step 3: Process files
    try:
        process_files(source_folder, append_string,toreplace,START_or_END)
        msgbox(f"Successfully renamed files!", "Success")
    except Exception as e:
        error(str(e))


def process_files(source_folder, append_string,toreplace,START_or_END):
    """Create subfolder and copy files with modified names"""
    # Create subfolder path
    subfolder_path = os.path.join(source_folder, append_string)
    
    # Create subfolder if it doesn't exist
    # if not os.path.exists(subfolder_path):
    #     os.makedirs(subfolder_path)
    
    # Get all files in source folder
    files = [f for f in os.listdir(source_folder) 
             if os.path.isfile(os.path.join(source_folder, f))]
    
    if not files:
        raise Exception("The selected folder does not contain any files.")
    
    # Copy files with appended names
    for filename in files:
        source_file_path = os.path.join(source_folder, filename)
        
        # Create new filename with appended string
        name, extension = os.path.splitext(filename)
        if START_or_END == 'START':
            new_filename = f"{append_string}{name.replace(toreplace,'')}{extension}" # can add a separator if necessary
        elif START_or_END == 'END':
            new_filename = f"{name.replace(toreplace,'')}{append_string}{extension}" # can add a separator if necessary

        destination_file_path = os.path.join(subfolder_path, new_filename)
        
        # Copy file to subfolder with new name
        # os.rename(source_file_path, destination_file_path) # if new folder needs to be created
        os.rename(source_file_path, os.path.join(source_folder,new_filename))
if __name__ == "__main__":
    main()
