import os
import wx
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
    files = [f for f in sorted(os.listdir(source_folder)) 
             if os.path.isfile(os.path.join(source_folder, f))]
    
    if not files:
        raise Exception("The selected folder does not contain any files.")
    # Copy files with appended names
    print(source_folder)
    print(files)
    for filename in files:
        # Create new filename with appended string
        name, extension = os.path.splitext(filename)
        if name + extension == "desktop.ini":
            continue # skips to next iteration. desktop.ini shows up when you change a folder's appearance
        if '_' not in name :
            print("exitted cuz no underscore",name)
            return
        thedate = name.split('_')[3][:9] # to get YYYYMMDD
        # N864A6_ch1_main_20250714103626_20250714110000
        cage_number = name.split('_')[1].replace('ch','')
        letter_ord_value = 97
        print(filename)
        while os.path.exists(os.path.join(source_folder,f"{cage_number}{chr(letter_ord_value)}_{thedate}{extension}")) and letter_ord_value < 123:
            letter_ord_value += 1
        else:
            os.rename(os.path.join(source_folder,filename),os.path.join(source_folder,cage_number + chr(letter_ord_value)+ extension))
        os.startfile(source_folder)

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
        wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    main()
