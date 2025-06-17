import os
import shutil
import wx
from common.common import windowpath,select_folder
def main():
    # Initialize wx application
    app = wx.App(False)
    
    # Step 1: Ask for folder directory
    source_folder = windowpath()
    if not os.path.isdir(source_folder):
        source_folder = select_folder()
    if not source_folder:
        return
    
    # Step 2: Ask for string input
    toreplace = get_string_input("Str to replace",'replace')
    append_string = get_string_input("Enter string to append to filenames:", 
                            "String Input")
    if not append_string:
        append_string = ''
    
    # Step 3: Process files
    try:
        process_files(source_folder, append_string,toreplace)
        wx.MessageBox(f"Successfully copied files to {append_string} folder with appended string!", 
                      "Success", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        print(f'Error: {str(e)}')
        wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def get_string_input(question,title):
    """Show text input dialog for string"""
    with wx.TextEntryDialog(None, question,title) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            input_string = dlg.GetValue().strip()
            if not input_string:
                # wx.MessageBox("Please enter a valid string!", "Warning", 
                #               wx.OK | wx.ICON_WARNING)
                return ''
                
            # Remove invalid filename characters
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                input_string = input_string.replace(char, '')
            if input_string =='xx':
                return ''
            else:
                return input_string
        return None

def process_files(source_folder, append_string,toreplace):
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
        new_filename = f"{name.replace(toreplace,'')}{append_string}{extension}" # can add a separator if necessary
        destination_file_path = os.path.join(subfolder_path, new_filename)
        
        # Copy file to subfolder with new name
        # os.rename(source_file_path, destination_file_path) # if new folder needs to be created
        os.rename(source_file_path, os.path.join(source_folder,new_filename))
if __name__ == "__main__":
    main()
