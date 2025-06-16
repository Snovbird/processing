import os
import wx
import pyperclip
from common.common import select_folder,windowpath


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
            return input_string
        return None

def name_cages(source_folder):
    """Create subfolder and copy files with modified names"""    
    # Get all files in source folder
    files = [f for f in os.listdir(source_folder) 
             if os.path.isfile(os.path.join(source_folder, f))]
    
    if not files:
        raise Exception("The selected folder does not contain any files.")
    # Copy files with appended names
    for filename in files:
        # Create new filename with appended string
        name, extension = os.path.splitext(filename)
        if '_' not in name:
            return
        a = name.split('_')[1].replace('ch','')
        c = 97
        print(filename)
        while os.path.exists(os.path.join(source_folder,a + chr(c) + extension)) and c < 123:
            c +=1
        else:
            os.rename(os.path.join(source_folder,filename),os.path.join(source_folder,a + chr(c)+ extension))
        os.startfile(source_folder)

def main():
    # Initialize wx application
    app = wx.App(False)
    
    # Step 1: Ask for folder directory
    currentwindow = windowpath()
    print(currentwindow)
    if os.path.isdir(currentwindow): # is it a file explorer window and is the setting to show full path in window name active (if not → else)
        source_folder = currentwindow
    else:
        source_folder = select_folder()
    if not source_folder:
        return
        
    # Step 3: Process files
    try:
        name_cages(source_folder)
    except Exception as e:
        wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    main()
