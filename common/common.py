import os
import wx

if __name__ == "__main__":
    from exceptions import *
# Get the absolute path to the directory containing this file (common.py)
COMMON_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_PATH = os.path.dirname(COMMON_CURRENT_DIR)
# This makes file access independent of where the script is run from.
# Define the path to data.json, assuming it's in the same directory as this script.
JSON_PATH = os.path.join(COMMON_CURRENT_DIR, 'data.json')

# no need to import modules present in __init__ (will be run first) # NOT SURE ABOUT THAT ACTUALLY
# answer = CustomDialog(None, title="", message="", option1="", option2="")

def windowpath() -> str:
    import win32gui
    window = win32gui.GetForegroundWindow()
    return str(win32gui.GetWindowText(window)).replace(' - File Explorer','').replace("\\\\","/")

def custom_dialog(msg="",title='',op1="yes",op2="No",op3=None,dimensions:tuple[int,int] = (300, 150)) -> str|None:

    class custom_dialog(wx.Dialog):
        def __init__(self, parent, title, message, option1="Proceed", option2="Skip",option3=None):
            super().__init__(parent, title=title, size=dimensions, style=wx.DEFAULT_DIALOG_STYLE)
            
            # Create a vertical box sizer for layout
            vbox = wx.BoxSizer(wx.VERTICAL)
            
            # Add the message text
            message_label = wx.StaticText(self, label=message, style=wx.ALIGN_CENTER)
            vbox.Add(message_label, 1, wx.ALL | wx.EXPAND, 10)
            
            # Create a horizontal box sizer for the buttons
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            
            # Add the first button
            self.option1_btn = wx.Button(self, label=option1)
            self.option1_btn.Bind(wx.EVT_BUTTON, self.on_option1)
            hbox.Add(self.option1_btn, 1, wx.ALL | wx.EXPAND, 5)
            
            # Add the second button
            self.option2_btn = wx.Button(self, label=option2)
            self.option2_btn.Bind(wx.EVT_BUTTON, self.on_option2)
            hbox.Add(self.option2_btn, 1, wx.ALL | wx.EXPAND, 5)
            if option3:
                self.option3_btn = wx.Button(self, label=option3)
                self.option3_btn.Bind(wx.EVT_BUTTON, self.on_option3)
                hbox.Add(self.option3_btn, 1, wx.ALL | wx.EXPAND, 5)


            # Add the button sizer to the main sizer
            vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)
            
            # Set the sizer for the dialog
            self.SetSizer(vbox)
            
            # Center the dialog on the screen
            self.Centre()
            
            # Variable to store the result
            self.result = None

        def on_option1(self, event):
            """Handle the first button click."""
            self.result = self.option1_btn.GetLabel()  # Store the button label as the result
            self.EndModal(wx.ID_OK)  # Close the dialog with OK status

        def on_option2(self, event):
            """Handle the second button click."""
            self.result = self.option2_btn.GetLabel()  # Store the button label as the result
            self.EndModal(wx.ID_CANCEL)  # Close the dialog with Cancel status
        def on_option3(self, event):
            """Handle the second button click."""
            self.result = self.option3_btn.GetLabel()  # Store the button label as the result
            self.EndModal(wx.ID_CANCEL)  # Close the dialog with Cancel status
        app = wx.App(False)  # Create the wx.App instance
    
    app = wx.App()
    # Create the dialog
    if op3:
        op3 = f"{op3}"
    dialog = custom_dialog(None, title=title, message=msg, option1=f'{op1}', option2=f'{op2}',option3=op3)
    
    # Show the dialog modally and get the result
    if dialog.ShowModal() == wx.ID_OK:
        dialog.Destroy()  # Clean up the dialog
        return dialog.result
    else:
        dialog.Destroy()  # Clean up the dialog
        return dialog.result

def select_folder(title="Choose a directory",path='') -> str|None:
    """Show folder selection dialog and return selected path"""
    
    app = wx.App(False)

    def pathDNE():
        with wx.DirDialog(None, title, 
                        style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                folder_path = dlg.GetPath()
                return folder_path
            return None
    if path:
        try:
            with wx.DirDialog(None, title, defaultPath=path,style=wx.DD_DEFAULT_STYLE) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    folder_path = dlg.GetPath()
                    return folder_path
        except:
            return pathDNE()
    else:
        return pathDNE()

def clear_gpu_memory() -> bool:
    import subprocess
    try:
        # Reset GPU clocks temporarily to help clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False
    
def select_video(title:str="Select videos",path:str='',avi:bool = False) -> list[str]:
    
    app = wx.App(False)

    def pathDNE():
        with wx.FileDialog(
            None,
            message=title,
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        ) as file_dialog:
            
            # Show the dialog and check if user clicked OK
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                
                return []  # Return empty list if canceled
                
            # Get the selected paths
            video_paths = file_dialog.GetPaths()
            return video_paths
        
    # Create wildcard string for mp4 files only
    if avi:
        wildcard = "Video files (*.mp4;*.avi)|*.mp4;*.avi" #"Video Files (*.mp4)|*.mp4" #"Video Files (*.mp4;*.avi;*.mov;*.mkv;*.webm)|*.mp4;*.avi;*.mov;*.mkv;*.webm"
    else: # mp4 only
        wildcard = "Video Files (*.mp4)|*.mp4"
    
    try:
        import os
        os.path.isdir(path)
        isadir = True
    except:
        isadir = False
    if isadir:
        try:
            with wx.FileDialog(
                None,
                message=title,
                defaultDir=path,
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
            ) as file_dialog:
                
                # Show the dialog and check if user clicked OK
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return []  # Return empty list if canceled
                    
                # Get the selected paths
                video_paths = file_dialog.GetPaths()

                return video_paths
        except Exception as e:
            custom_dialog(msg="here " + str(e))
            return pathDNE()
    else:
        return pathDNE()

def select_anyfile(title="Select files",path='',specific_ext:list[str] | str=None) -> list[str]:
    """
    Returns a **`LIST`**

    
    Default wildcard: Any files (\*.\*)|\*.\*

    **If specific_ext**:
    provide extensions as ["txt","xlsx","csv"] without periods 

    Args:
    title: Message displayed in the topleft of the explorer window
    path: start directory where the navigation begins (startpath)
    specific_ext: The extension(s) name(s) WITHOUT PERIOD displayed while browsing 
    """
    app = wx.App(False)
    if not specific_ext:
        wildcard = "Any files (*.*)|*.*"
    elif type(specific_ext) == str:
        ext_filtered = ';*.'.join([specific_ext.replace(".",'')])
        wildcard = f"Files (*.{ext_filtered})|*.{ext_filtered}"

    else: # string or tuple
        ext_filtered = ';*.'.join([ext.replace(".",'') for ext in specific_ext])
        wildcard = f"Files (*.{ext_filtered})|*.{ext_filtered}"
    def pathDNE():
        app = wx.GetApp()
        if not app:
            app = wx.App(False)
        with wx.FileDialog(
            None,
            message=title,
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        ) as file_dialog:
            
            # Show the dialog and check if user clicked OK
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return []  # Return empty list if canceled
                
            # Get the selected paths
            file_paths = file_dialog.GetPaths()
            files_str = '\n' + '\n'.join(file_paths)
            print(f"{title.replace('?','').replace(':','')}: {files_str}")
            return file_paths
    # Create the file dialog
    if path:
        try:
            with wx.FileDialog(
                None,
                message=title,
                defaultDir=path,
                wildcard=wildcard,
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
            ) as file_dialog:
                
                # Show the dialog and check if user clicked OK
                if file_dialog.ShowModal() == wx.ID_CANCEL:
                    return []  # Return empty list if canceled
                    
                # Get the selected paths
                video_paths = file_dialog.GetPaths()
                return video_paths
        except:
            return pathDNE()
    else:
        return pathDNE()

def askint(msg:str="Enter an integer:", title:str="Integer Input", fill:str|int=0) -> int:
    """Open a dialog to ask for an integer, always on top."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=f"{fill}", style=wx.OK | wx.CANCEL | wx.CENTRE | wx.CAPTION | wx.CLOSE_BOX)
    dlg.Centre()
    import ctypes
    ctypes.windll.user32.SetWindowPos(dlg.GetHandle(), -1, 0, 0, 0, 0, 3)
    dlg.RequestUserAttention()
    
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        rawresult = dlg.GetValue()
        try:
            result = int(rawresult)  # Convert the input to an integer
            dlg.Destroy()
            app.Destroy()
            print(f"{msg.replace('?','').replace(':','')}: {result}")
            return result
        except ValueError:
            dlg.Destroy()
            error(f"{rawresult} is not a valid value. Please enter a valid integer.")
            app.Destroy()
            
            return askint(msg=msg, title=title, fill=fill)
    
    dlg.Destroy()
    app.Destroy()
    return None

def askstring(msg="Enter a string:",title="String Input",fill='') -> str:
    
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=f'{fill}',style= wx.OK | wx.CANCEL | wx.CENTRE | wx.CAPTION | wx.CLOSE_BOX)
    dlg.Centre()
    import ctypes
    ctypes.windll.user32.SetWindowPos(dlg.GetHandle(), -1, 0, 0, 0, 0, 3)
    dlg.RequestUserAttention()
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        result = dlg.GetValue()  # Get the entered string
        print(f"{msg.replace('?','').replace(':','')}: {result}")
        return result
    dlg.Destroy()  # Clean up the dialog
    
    return None

def makefolder(file_or_folder_path:str, foldername:str='',start_at_1:bool=True,hide:bool=False,count:int=1,) -> str:
    """
    Args:
        file_or_folder_path (str): The path to the file or folder.
        foldername (str): The name of the created folder. Default is empty. If start_at_1 is False, first folder will be named `-`. Subsequent folders will be named after their count value  
        start_at_1 (bool): if False, first unique created folder in dir does not have "-1" in its name. If exists, will have `-2` appended. Default is `True`.
        hide (bool): created folder will be hidden. Default is `False`.
        count (int): Initial count for folder. If start_at_1 is false,  first `-count` will be hidden, but following will keep this sequence start. Default is `-1`.
    
    """
    
    import os
    # Get directory containing the file
    if os.path.isdir(file_or_folder_path):
        folder_path = file_or_folder_path
    else:
        folder_path = os.path.dirname(file_or_folder_path)
        # file_name = os.path.splitext(os.path.basename(file_or_folder_path))[0]    # Get filename without extension
    
    # Create folder name
    if not start_at_1 and count == 1:
        new_folder_name = f"{foldername if foldername != '' else '-'}"
    else:
        if foldername == '':
            new_folder_name = f"{count}"
        else:
            new_folder_name = f"{foldername.replace('-','')}-{count}"
    # Create full path to new folder
    new_folder_path = os.path.join(folder_path, new_folder_name)
    
    # Create the folder if it doesn't exist
    if os.path.exists(new_folder_path):
        return makefolder(file_or_folder_path,foldername,hide=hide,count=count+1)
    else:
        os.makedirs(new_folder_path)
        if hide:
            import subprocess
            import sys
            creationflags = 0
            if sys.platform == 'win32':
                creationflags = subprocess.CREATE_NO_WINDOW
            subprocess.run(['attrib', '+h', new_folder_path], check=True, creationflags=creationflags)

        # print(f"Created folder: {new_folder_path}")
    return new_folder_path

def makefolderpath(file_or_folder_path:str, foldername:str='',start_at_1:bool=True,hide:bool=False,count:int=1,) -> str:
    """
    Same as makefolder but returns the path to the created folder instead of creating it. Does not check if path exists.
    """
    import os
    # Get directory containing the file
    if os.path.isdir(file_or_folder_path):
        folder_path = file_or_folder_path
    else:
        folder_path = os.path.dirname(file_or_folder_path)
    
    # Create folder name
    if not start_at_1 and count == 1:
        new_folder_name = f"{foldername if foldername != '' else '-'}"
    else:
        if foldername == '':
            new_folder_name = f"{count}"
        else:
            new_folder_name = f"{foldername.replace('-','')}-{count}"
    # Create full path to new folder
    new_folder_path = os.path.join(folder_path, new_folder_name)
    
    return new_folder_path

def get_duration(video_path: str) -> tuple[float, str] | None:
    """
    Get the duration of a video file
    
    Args:
        video_path: Path to the video file
        
    Returns:
        A tuple containing (frames,seconds, formatted_time) or None if error
    """
    import cv2
    import datetime

    # Check if file exists
    if not os.path.isfile(video_path):
        print(f"Error finding video duration: File '{video_path}' does not exist")
        return None
        
    # Create video capture object
    video = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not video.isOpened():
        error(f"Could not find duration for video. Unable to open: '{video_path}'")
        return None
    
    # Count the number of frames
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # Calculate duration in seconds
    seconds = frames / fps
    
    # Format time as HH:MM:SS (keep the colons!)
    formatted_time = str(datetime.timedelta(seconds=int(seconds)))
    
    # Release the video object
    video.release()
    
    return frames, seconds, formatted_time

def msgbox(msg:str, title:str=' ', timeout:int=None):
    """
    display a message
    
    :param msg: content
    :type msg: str
    :param title: title displayed in top left
    :type title: str
    :param timeout: time in seconds before auto close. Default keeps window open
    :type timeout: int
    """
    app = wx.GetApp()
    if not app:
        app = wx.App(False)  # Create the wx.App instance

    if timeout:
        dlg = wx.MessageDialog(None, f"{msg}", f"{title}", wx.OK | wx.ICON_INFORMATION)
        timer = wx.Timer(dlg)
        dlg.Bind(wx.EVT_TIMER, lambda event: dlg.EndModal(wx.ID_OK), timer)
        timer.Start(timeout * 1000, oneShot=True)
        dlg.ShowModal()
        dlg.Destroy()
    else:
        wx.MessageBox(f"{msg}", f"{title}", wx.OK | wx.ICON_INFORMATION)

def error(msg:str,title:str="ERROR"):
    

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(f"Error: {msg}", f"{title}", wx.OK | wx.ICON_ERROR)

def find_folder_path(foldername:str) -> str:
    import json

    # First, read the JSON data
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
    except FileNotFoundError:
        jsondata = {"folder_dirs": {},"values":{}}
    
    def longfind():
        if custom_dialog(f"Cannot find {foldername}, begin full search?","Long search") == "no":
            return
        desktop_path = os.path.expanduser("~")
        for root, dirs, files in os.walk(desktop_path):
            if foldername in dirs:
                output_path = os.path.join(root, foldername)
                # Update the JSON data in memory
                if "folder_dirs" not in jsondata:
                    jsondata["folder_dirs"] = {}
                jsondata['folder_dirs'][foldername] = output_path
                
                # Write the updated JSON data back to the file
                with open(JSON_PATH, 'w') as j:
                    json.dump(jsondata, j,indent=4)
                return output_path
        error(f"No folder with the name {foldername}")
        return None

    try:
        findfolder = jsondata['folder_dirs'][foldername]
        if os.path.exists(findfolder):
            return findfolder
        else:
            return longfind()
    except KeyError:
        return longfind()
    
def findval(valuename:str):
    import json

    # First, read the JSON data
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/invalid, there's no value to find.
        return 

    if not isinstance(jsondata, dict):
        return None

    # Use .get() for safer access. Return None if 'values' or valuename doesn't exist.
    return jsondata.get('values', {}).get(valuename, "DOES NOT EXIST")
    # return jsondata.get('values', {}).get(valuename, None)

def assignval(valuename:str,value):
    import json
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
        jsondata['values'][valuename] = value
        
        with open(JSON_PATH, 'w') as j:
            json.dump(jsondata,j,indent=4)
    except Exception as e:
        print(f"Failed to assign {value} to {valuename}.\nError: {e}")

def dropdown(choices: list[str], title='', icon_name=None,hide:tuple[str]=(None,),return_index:bool=False) -> str:
    """
    Args:
    choices: list of string (options) to display in the dropdown
    title: Title in the top left of the window
    icon_name:  **`star`**, **`check`**
    """

    app = wx.GetApp()
    if hide[0]:
        for obj in hide:
            if obj in choices:
                choices.remove(obj)
    if not app:
        app = wx.App(False)
        created_app = True
    else:
        created_app = False

    # Create a dialog instead of a frame for modal behavior
    if icon_name:
        dialog = wx.Dialog(None, title=title, size=(315, 150))
        icon_path = os.path.join(SCRIPTS_PATH,'icons',f"{icon_name}.ico")
        if os.path.exists(icon_path):
            try:
                icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)
                dialog.SetIcon(icon)
            except Exception as e:
                print(f"Failed to load icon: {e}")
    else:
        dialog = wx.Dialog(None, title=title, size=(315, 150))

    dialog.CenterOnScreen()
    
    panel = wx.Panel(dialog)
    dropdown_ctrl = wx.Choice(panel, choices=choices, pos=(50, 20), size=(200, -1))
    dropdown_ctrl.SetSelection(0)
    
    selected_item = [None]
    
    button_width = 70
    button_spacing = 10
    total_button_width = (button_width * 2) + button_spacing
    start_x = (300 - total_button_width) // 2
    
    ok_button = wx.Button(panel, label="OK", pos=(start_x, 70), size=(button_width, 30))
    cancel_button = wx.Button(panel, label="Cancel", pos=(start_x + button_width + button_spacing, 70), size=(button_width, 30))
    
    def on_key_press(event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            selected_item[0] = dropdown_ctrl.GetString(dropdown_ctrl.GetSelection())
            dialog.EndModal(wx.ID_OK)
        else:
            event.Skip()
    
    def on_ok(event):
        selected_item[0] = dropdown_ctrl.GetString(dropdown_ctrl.GetSelection())
        dialog.EndModal(wx.ID_OK)
    
    def on_cancel(event):
        selected_item[0] = None
        dialog.EndModal(wx.ID_CANCEL)
    
    dialog.Bind(wx.EVT_CHAR_HOOK, on_key_press)
    ok_button.Bind(wx.EVT_BUTTON, on_ok)
    cancel_button.Bind(wx.EVT_BUTTON, on_cancel)
    
    # Always use ShowModal for dialogs
    dialog.ShowModal()
    dialog.Destroy()
    
    return selected_item[0]

def hhmmss_to_seconds(time_str:str) -> int:
    """Convert HHMMSS string to total seconds"""
    # Ensure the string is 6 characters long (pad with leading zeros if needed)
    if type(time_str) != str:
        try:
            str(time_str)
        except Exception as e:
            error("Error wrong input:", str(e))
            return
    
    # runs anyway 
    time_str = time_str.zfill(6)
    
    # Extract hours, minutes, seconds
    hours = int(time_str[0:2])
    minutes = int(time_str[2:4])
    seconds = int(time_str[4:6])
    
    # Convert to total seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds
    
def seconds_to_hhmmss(seconds:int) -> str:
    """Convert seconds to HHMMSS string format"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    hhmmss_string = f"{hours:02d}{minutes:02d}{remaining_seconds:02d}".zfill(6)

    return hhmmss_string

def format_time_colons(time_input:str) -> str:
    """
    Format the time input to HH:MM:SS.
    
    Args:
        time_input (str): The input time as a string without colons.
    
    Returns:
        str: Formatted time as HH:MM:SS.
    """
    time_input = time_input.strip()
    
    if time_input.isdigit():
        time_input = time_input.zfill(6) # or f"{time_input:06d}" would've also worked IF WE HAD AN INTEGER AND NOT A STRING
        return f"{time_input[:-4]}:{time_input[-4:-2]}:{time_input[-2:]}"
    else:
        return time_input  # Return the original input if it's not valid
    
def wrap(text_input:str,text_to_wrap:str) -> str:
    '''
    To a *`string`*: appends on both sides of a 'text_input' another string 'text_to_wrap'
    '''
    return f"{text_to_wrap}{text_input}{text_to_wrap}"

def remove_other(stringinput:str,allowed:list[str]=["."]) -> str:
    """
    Cleans a *`string`* to remove characters that arent **PERIODS** or **NUMBERS**
    """
    clean_string = ""
    for char in stringinput:
        if char.isdigit():
            clean_string += char
        elif char in allowed:
            clean_string += char
    return clean_string

def group_from_end(data: list, chunk_size: int) -> list[list[str]]:
    """
    Groups a list into sublists of a given size, starting from the end.
    The first sublist may be smaller if the total number of items is not
    a multiple of chunk_size.

    Example:
    group_from_end(list(range(16)), 7)
    >> [[0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]]
    """
    if not data:
        return []
    
    # Reverse the list to group from the "start" (which is the original end)
    reversed_list = data[::-1]
    # Create chunks from the reversed list, then reverse the chunks and their contents
    temp_chunks = [reversed_list[i:i + chunk_size] for i in range(0, len(reversed_list), chunk_size)]
    return [chunk[::-1] for chunk in temp_chunks[::-1]]

def is_dir(path:str) -> bool:
    try:
        return os.path.isdir(path)
    except:
        return False

def is_file(path:str) -> bool:
    try:
        return os.path.isfile(path)
    except:
        return False
    
def path_exists(path:str) -> bool:
    try:
        return os.path.exists(path)
    except:
        return False

def get_date_yyyymmdd() -> str:
    """
    Returns: 
    Today's date formatted as MM-DD.
    ## Also:
    Assigns this date to the value "dates" in the json 
    """
    from datetime import date
    # Get today's date
    today = date.today()
    # Format the date as MM-DD
    formatted_date = today.strftime("%Y%m%d")
    alldates = findval("dates")
    if alldates[-1] != formatted_date:
        alldates.append(formatted_date)
        assignval("dates",alldates)
        print(f"Added date: {formatted_date}")
    return formatted_date

def list_files(dir:str) -> list[str]:
    """
    files names (ex: ['apples.mp4', 'banana.mp4'])
    """
    if os.path.isdir(dir):
        return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folders(dir:str) -> list[str]:
    """
    folder names (ex: ['apples', 'banana'])
    """
    if os.path.isdir(dir):
        return [folder for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]

def list_filespaths(dir:str) -> list[str]:
    """
    returns: the FULL path of files in a directory

    ex: `C:/users/me/apples.mp4, C:/users/me/banana.mp4`
    """
    return [os.path.join(dir, file) for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folderspaths(dir:str) -> list[str]:
    """
    returns: the FULL path of folders in a directory

    ex: `C:/users/me/apples/, C:/users/me/banana/`
    """
    return [os.path.join(dir, folder) for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]

def unhide_folder(dir:str):
    import sys,subprocess
    creationflags = 0
    if sys.platform == 'win32':
        creationflags = subprocess.CREATE_NO_WINDOW
                
    subprocess.run(['attrib', '-h', dir], check=True, creationflags=creationflags)

def is_date(date_string:str) -> bool:
    """Simple date checker for most common formats"""
    from datetime import datetime
    common_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y%m%d']
    
    for fmt in common_formats:
        try:
            datetime.strptime(date_string.strip(), fmt)
            return True
        except ValueError:
            continue
    return False

def wrap(input_str:str,count:int=20,wrap:str="*",printq:bool=True):
    """
    Args:
    input_str: the middle component of the string
    count: the amount of characters on either side of the middle string
    wrap: the character wrapping the input. Default is asterisk "*"
    printq: yes or no? do we print the wrapped string. Default is yes
    """
    total = count *2 + len(input_str)
    wrapped:str = f"{input_str:wrap^total}"
    if printq:
        print(wrapped)
    return wrapped
    
def avg(list_values: list[int | float]) -> str:
    from fractions import Fraction
    
    if not list_values:
        raise ValueError("Cannot calculate average of empty list")
    
    total = sum(list_values)
    count = len(list_values)
    
    # Create fraction and it will automatically be reduced
    average_fraction:Fraction = Fraction(total, count)

    normal_float:float = total / count 
    return average_fraction, normal_float

def simple_file_walk(folder,filefunc = None) -> tuple[ set[str],set[str]] | int:
    """Simple version - just print all files"""
    if filefunc:
        count = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                filefunc(os.path.join(root, file))
                count +=1
        return count
    else:
        filepaths = set()
        dirspaths = set()

        for root, dirs, files in os.walk(folder):
            for file in files:
                filepaths.add(os.path.join(root, file))
            for dir in dirs:
                dirspaths.add(os.path.join(root, dir))
        return filepaths,dirspaths
          
def letter(text:str) -> str:
    """
    Remove all non-letter characters
    """
    return ''.join(char for char in text if char.isalpha())

def check(options:list[str],msg:str="Choose options",title:str="Selections") -> list[str]:

    app = wx.App(False)
    
    dialog1=wx.MultiChoiceDialog(None,message=msg,caption=title,choices=options)
    if dialog1.ShowModal()==wx.ID_OK:
        indexes:list[int] = dialog1.GetSelections() # returns indexes such as [0,1]
        return [options[index] for index in indexes]

def hex_to_rgb(hex_color:str):
    
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb

def rgb_to_hex(rgb:tuple[int,int,int]):

    hex = '#' + ''.join(f'{c:02x}' for c in rgb)
    return hex

def color_tuple_generator():
    """
    Generator that yields RGB color tuples starting with extreme values (0, 255),
    then progressively adding intermediate values by halving intervals.
    
    Level 1: {0, 255} combinations
    Level 2: {0, 127, 255} combinations  
    Level 3: {0, 63, 127, 191, 255} combinations
    And so on...
    
    Yields: RGB tuples like (0,0,255), (255,255,0), then (0,0,127), etc.
    """
    used_colors = set()
    
    # Start with extreme values
    current_values = [0, 255]
    
    while len(current_values) <= 32:  # Reasonable limit to prevent excessive computation
        # Generate all RGB combinations for current set of values
        level_colors = []
        
        for r in current_values:
            for g in current_values:
                for b in current_values:
                    color = (r, g, b)
                    if color not in used_colors:
                        level_colors.append(color)
                        used_colors.add(color)
        
        # Yield colors from this level
        for color in level_colors:
            yield color
        
        # Generate next level by adding midpoints between adjacent values
        next_values = list(current_values)
        
        for i in range(len(current_values) - 1):
            midpoint = (current_values[i] + current_values[i + 1]) // 2
            if midpoint not in next_values:
                next_values.append(midpoint)
        
        # Sort values for next iteration
        next_values.sort()
        
        # If no new values were added, we're done
        if len(next_values) == len(current_values):
            break
            
        current_values = next_values

def get_extreme_colors(n):
    """
    Get the first n extreme colors.
    
    Args:
        n (int): Number of colors to generate
        
    Returns:
        list: List of RGB tuples
    """
    colors = []
    generator = color_tuple_generator()
    
    for _ in range(n):
        try:
            colors.append(next(generator))
        except StopIteration:
            break
    
    return colors

def simple_dropdown(choices,msg='',title='',return_index = False):
    """Simple dropdown function using wx.SingleChoiceDialog"""
    app = wx.App(False)

    # Create dropdown dialog
    dialog = wx.SingleChoiceDialog(
        None,
        message=msg,
        caption=title,
        choices=choices,
        style=wx.CHOICEDLG_STYLE | wx.STAY_ON_TOP
    )
    
    selection = None
    # Show dialog and get result
    if dialog.ShowModal() == wx.ID_OK:
        if return_index:
            selection = dialog.GetSelection() 
        else:
            selection = dialog.GetStringSelection()
            
    dialog.Destroy()
    app.Destroy()
    print(f"{msg.replace('?','').replace(':','')}: {selection}")
    return selection

def list_files_ext(dir:str,ext:str) -> list[str]:
    """
    files names (ex: ['apples.mp4', 'banana.mp4'])
    """
    if os.path.isdir(dir):
        return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file)) and file.lower().endswith(ext.lower())]
    
def abs(number:int) -> int:
    """Returns the absolute value of an integer"""
    if number < 0:
        return -number
    return number

def delete_folder(folder_path:str) -> bool:
    for file in list_filespaths(folder_path):
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete file {file}: {e}")
            return False
    else:
        try:
            os.rmdir(folder_path)
            return True
        except Exception as e:
            print(f"Failed to delete folder {folder_path}: {e}")
            return False
        
def grid_selector(strings_list, options_list, title='Selection', message='Select options for each item'):
    """
    Create a grid selection window with radio buttons
    
    Args:
        strings_list: List of strings to display in first column
        options_list: List of options to display as column headers
        title: Window title
        message: Message to display at top
        
    Returns:
        dict: Dictionary where keys are strings and values are selected options
    """
    import wx
    
    app = wx.App(False)
    
    # Larger sizing for better visibility
    col_width = 150
    row_height = 45
    header_height = 35
    message_height = 40
    button_height = 40
    padding = 20
    
    # Calculate window size based on content
    num_cols = len(options_list) + 1
    num_rows = len(strings_list) + 1
    
    content_width = num_cols * col_width
    content_height = (num_rows * row_height) + header_height + message_height + button_height
    
    window_width = content_width + (padding * 2)
    window_height = content_height + (padding * 3)
    
    # Create dialog
    dialog = wx.Dialog(None, title=title, size=(window_width, window_height))
    dialog.CenterOnScreen()
    
    # Main panel
    panel = wx.Panel(dialog)
    main_sizer = wx.BoxSizer(wx.VERTICAL)
    
    # Add message at top with larger font
    message_label = wx.StaticText(panel, label=message)
    message_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    message_label.SetFont(message_font)
    main_sizer.Add(message_label, 0, wx.ALL | wx.CENTER, 10)
    
    # Create grid sizer with larger spacing
    grid_sizer = wx.FlexGridSizer(num_rows, num_cols, 8, 8)
    
    # Set minimum column widths
    for col in range(num_cols):
        grid_sizer.AddGrowableCol(col, 1)
    
    # Row 1: Headers
    # Empty cell in top-left
    grid_sizer.Add(wx.StaticText(panel, label=""), 0, wx.ALIGN_CENTER)
    
    # Add option headers with larger font
    header_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    for option in options_list:
        header = wx.StaticText(panel, label=option)
        header.SetFont(header_font)
        grid_sizer.Add(header, 0, wx.ALIGN_CENTER | wx.ALL, 5)
    
    # Store radio buttons in a 2D structure for proper navigation
    radio_grid = []  # [row][col] structure
    radio_groups = {}
    
    # Larger font for string labels
    label_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    
    for row_idx, string_item in enumerate(strings_list):
        # First column: string label with larger font
        label = wx.StaticText(panel, label=string_item)
        label.SetFont(label_font)
        grid_sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        
        # Create row for radio buttons
        radio_row = []
        radio_groups[string_item] = []
        
        for col_idx, option in enumerate(options_list):
            # Each row needs its own radio button group
            # Use a unique ID for each radio button group
            if col_idx == 0:
                # First radio button in each row starts a new group
                radio = wx.RadioButton(panel, style=wx.RB_GROUP, size=(25, 25))
            else:
                # Subsequent radio buttons in the same row
                radio = wx.RadioButton(panel, size=(25, 25))
            
            radio_groups[string_item].append(radio)
            radio_row.append(radio)
            
            # Set first option as default for first row only
            if row_idx == 0 and col_idx == 0:
                radio.SetValue(True)
            
            grid_sizer.Add(radio, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        radio_grid.append(radio_row)
    
    # Add grid to main sizer
    main_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, padding)
    
    # Buttons with larger size
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    ok_button = wx.Button(panel, wx.ID_OK, "OK", size=(80, 35))
    cancel_button = wx.Button(panel, wx.ID_CANCEL, "Cancel", size=(80, 35))
    
    # Larger button font
    button_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    ok_button.SetFont(button_font)
    cancel_button.SetFont(button_font)
    
    button_sizer.Add(ok_button, 0, wx.ALL, 8)
    button_sizer.Add(cancel_button, 0, wx.ALL, 8)
    main_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
    
    panel.SetSizer(main_sizer)
    
    # Enhanced keyboard navigation using 2D grid
    def on_key_down(event):
        keycode = event.GetKeyCode()
        focused = wx.Window.FindFocus()
        
        # Find current position in grid
        current_row = -1
        current_col = -1
        
        for row in range(len(radio_grid)):
            for col in range(len(radio_grid[row])):
                if radio_grid[row][col] == focused:
                    current_row = row
                    current_col = col
                    break
            if current_row != -1:
                break
        
        if current_row != -1 and current_col != -1:
            new_row = current_row
            new_col = current_col
            
            if keycode == wx.WXK_DOWN:
                # Move down one row, same column
                new_row = min(current_row + 1, len(radio_grid) - 1)
                
            elif keycode == wx.WXK_UP:
                # Move up one row, same column
                new_row = max(current_row - 1, 0)
                
            elif keycode == wx.WXK_RIGHT:
                # Move right one column, same row
                new_col = min(current_col + 1, len(radio_grid[current_row]) - 1)
                
            elif keycode == wx.WXK_LEFT:
                # Move left one column, same row
                new_col = max(current_col - 1, 0)
                
            elif keycode == wx.WXK_RETURN:
                # Trigger OK button
                ok_button.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED))
                return
            
            # Move focus and select new radio button
            if (new_row != current_row or new_col != current_col):
                new_radio = radio_grid[new_row][new_col]
                new_radio.SetFocus()
                new_radio.SetValue(True)
        
        event.Skip()
    
    # Bind keyboard events
    dialog.Bind(wx.EVT_CHAR_HOOK, on_key_down)
    
    # Set focus to first radio button
    if radio_grid and radio_grid[0]:
        radio_grid[0][0].SetFocus()
    
    # Fit the dialog to its contents
    main_sizer.Fit(dialog)
    dialog.SetMinSize(dialog.GetSize())
    
    # Initialize result dictionary
    result = {}
    
    # Show dialog and process result
    if dialog.ShowModal() == wx.ID_OK:
        # Collect selected options for each string
        for string_item in strings_list:
            selected_option = None
            for i, radio in enumerate(radio_groups[string_item]):
                if radio.GetValue():
                    selected_option = options_list[i]
                    break
            result[string_item] = selected_option
    else:
        # Return empty dict if cancelled
        result = {}
    
    dialog.Destroy()
    app.Destroy()
    return result

def attempt_delete(todelete:str, delete_interval=1):
    """
    While loop to intermitently attempt to delete a file. Prints errors
    Args:
        todelete: file or folder path to delete 
        delete_interval: Seconds between each attempt to delete `todelete` path
    """
    is_folder = is_dir(todelete)
    while True:
        try:
            if is_folder:
                delete_folder(todelete)
                return
            else:
                os.remove(todelete)
        except Exception as e:
            print(f"Error occured while deleteting {todelete}\nError:{e}")

def screenshot(video_path: str, frame_number: int, output_path: str = "screenshot.png",start_at_1=True) -> str:
    """
    Extract a specific frame from a video and save it as a PNG image. Will not overwrite existing files; instead, it appends a number to the filename.
    
    Args:
        video_path: Path to the MP4 video file
        frame_number: The exact frame number to capture
        output_path: Path for the output PNG file (default: "screenshot.png")
        start_at_1: If True, png is numbered from 1; if False, no numbering for the first unique image name
    
    Returns:
        screenshot png path
    """
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.path.dirname(video_path), output_path)

    import cv2

    filename, ext = os.path.splitext(os.path.basename(output_path))

    if start_at_1:
        c = 1
        output_path = os.path.join(os.path.dirname(output_path), f"{filename}{c}{ext}")
    
    while os.path.exists(output_path):
        c += 1
        output_path = os.path.join(os.path.dirname(output_path), f"{filename}{c}{ext}")

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return False
    
    # Set the frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    ret, frame = cap.read()
    
    if not ret:
        print(f"Error: Could not read frame {frame_number}")
        cap.release()
        return False
    
    # Save the frame as PNG
    cv2.imwrite(output_path, frame)
    
    # Clean up
    cap.release()
    
    print(f"{os.path.basename(video_path)} screenshot at frame {frame_number} saved to: {output_path}")
    return output_path
