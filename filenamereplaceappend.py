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
        START_or_END_or_REPLACE = custom_dialog(msg=f"Place string at the START, END of the file name or simply replace '{toreplace}'",
                                     title='START or END or REPLACE',
                                     op1="START",op2="END",op3="REPLACE")

    if not append_string:
        append_string = ''
        START_or_END_or_REPLACE = 'END'
    
    # Step 3: Process targets
    try:
        rename_files(source_folder, append_string,toreplace,START_or_END_or_REPLACE)
        msgbox(f"Successfully renamed targets!", "Success")
    except Exception as e:
        error(str(e))


def rename_files(source_folder, append_string,toreplace,START_or_END_or_REPLACE,file_or_folder=None):
    """Create subfolder and copy targets with modified names"""
    # Create subfolder path
    subfolder_path = os.path.join(source_folder, append_string)
    if not file_or_folder:
        file_or_folder = custom_dialog("Change file or folder names?","Target","File","Folder")
        if not file_or_folder:
            return
    # Create subfolder if it doesn't exist
    # if not os.path.exists(subfolder_path):
    #     os.makedirs(subfolder_path)
    
    # Get all targets in source folder
    if file_or_folder == 'File':
        
        targets = [f for f in os.listdir(source_folder) 
                if os.path.isfile(os.path.join(source_folder, f))]
    elif file_or_folder == 'Folder':
        targets = [f for f in os.listdir(source_folder) 
                if os.path.isdir(os.path.join(source_folder, f))]
    else:
        targets = ''
    
    if not targets:
        raise Exception(f"The selected folder does not contain any {file_or_folder}.")
    
    # Copy targets with appended names
    for filename in targets:
        source_file_path = os.path.join(source_folder, filename)
        
        # Create new filename with appended string
        name, extension = os.path.splitext(filename)
        if START_or_END_or_REPLACE == 'START':
            new_filename = f"{append_string}{name.replace(toreplace,'')}{extension}" # can add a separator if necessary
        elif START_or_END_or_REPLACE == 'END':
            new_filename = f"{name.replace(toreplace,'')}{append_string}{extension}" # can add a separator if necessary
        elif START_or_END_or_REPLACE == 'REPLACE':
            new_filename = f"{name.replace(toreplace,append_string)}{extension}"
            
        destination_file_path = os.path.join(subfolder_path, new_filename)
        
        # Copy file to subfolder with new name
        # os.rename(source_file_path, destination_file_path) # if new folder needs to be created
        os.rename(source_file_path, os.path.join(source_folder,new_filename))
if __name__ == "__main__":
    main()
