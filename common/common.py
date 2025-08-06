import os
import wx
# Get the absolute path to the directory containing this file (common.py)
COMMON_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to data.json, assuming it's in the same directory as this script.
# This makes file access independent of where the script is run from.
JSON_PATH = os.path.join(COMMON_CURRENT_DIR, 'data.json')

# no need to import modules present in __init__ (will be run first) # NOT SURE ABOUT THAT ACTUALLY
# answer = CustomDialog(None, title="", message="", option1="", option2="")

def windowpath() -> str:
    import win32gui
    window = win32gui.GetForegroundWindow()
    return str(win32gui.GetWindowText(window)).replace(' - File Explorer','').replace("\\\\","/")

def custom_dialog(msg="",title='',op1="yes",op2="No",op3=None,dimensions:tuple|int = (300, 150)) -> str:

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

def select_folder(title="Choose a directory",path='') -> str:
    """Show folder selection dialog and return selected path"""
    
    app = wx.App(False)

    def pathDNE():
        with wx.DirDialog(None, title, 
                        style=wx.DD_DEFAULT_STYLE) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                folder_path = dlg.GetPath()
                return folder_path
            return None
    # Create wildcard string for mp4 files only
    wildcard = "Video Files (*.mp4)|*.mp4" #"Video files (*.mp4;*.avi)|*.mp4;*.avi" #"Video Files (*.mp4)|*.mp4" #"Video Files (*.mp4;*.avi;*.mov;*.mkv;*.webm)|*.mp4;*.avi;*.mov;*.mkv;*.webm"
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

def select_anyfile(title="Select files",path='',specific_ext:list[str]=None) -> list[str]:
    """
    ##Default:
    Any files (*.*)|*.*
    ##If specific_ext list is provided:
    provide extensions as ["txt","xlsx","csv"] without periods 
    """
    app = wx.App(False)
    if not specific_ext:
        wildcard = "Any files (*.*)|*.*"
    else:
        ext_filtered = [ext.replace(".",'') for ext in specific_ext]
        wildcard = f"Files (*.{';*.'.join(specific_ext)})|*.{';*.'.join(specific_ext)}"
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

def askint(msg="Enter an integer:", title="Integer Input", fill='0') -> int:
    
    
    """Open a dialog to ask for an integer, always on top."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=str(fill), style=wx.OK | wx.CANCEL)
    dlg.Centre()
    
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        try:
            result = int(dlg.GetValue())  # Convert the input to an integer
            dlg.Destroy()
            app.Destroy()
            return result
        except ValueError:
            dlg.Destroy()
            wx.MessageBox("Invalid input. Please enter a valid integer.", "Error", 
                         wx.ICON_ERROR)
            app.Destroy()
            return askint(msg=msg, title=title, fill=fill)
    
    dlg.Destroy()
    app.Destroy()
    return None

def askstring(msg="Enter a string:",title="String Input",fill='') -> str:
    

    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=f'{fill}',style= wx.OK)
    dlg.Centre()
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        result = dlg.GetValue()  # Get the entered string
        print(f"Entered string: {result}")
        return result
    dlg.Destroy()  # Clean up the dialog
    return None

def makefolder(file_or_folder_path:str, foldername:str='',start_at_1:bool=True,hide:bool=False,count:int=1,) -> str:
    import os
    # Get directory containing the file
    if os.path.isdir(file_or_folder_path):
        folder_path = file_or_folder_path
    else:
        folder_path = os.path.dirname(file_or_folder_path)
        # file_name = os.path.splitext(os.path.basename(file_or_folder_path))[0]    # Get filename without extension
    
    # Create folder name
    if not start_at_1 and count == 1:
        new_folder_name = f"{foldername}"
    else:
        new_folder_name = f"{foldername}-{count}"

    # Create full path to new folder
    new_folder_path = os.path.join(folder_path, new_folder_name)
    # Check if folder exists and print debug info
    # print(f"Checking if folder exists: {new_folder_path}")
    # print(f"Folder exists: {os.path.exists(new_folder_path)}")
    
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

def get_duration(video_path: str) -> tuple[float, str] | None:
    """
    Get the duration of a video file
    
    Args:
        video_path: Path to the video file
        
    Returns:
        A tuple containing (frames,seconds, formatted_time) or None if error
    """
    import os
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
        print(f"Error: Could not open video '{video_path}'")
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

def msgbox(msg:str,title:str=' '):
    

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION)

def error(msg:str,title:str="ERROR"):
    

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(f"Error: {msg}", title, wx.OK | wx.ICON_ERROR)

def find_folder_path(foldername:str) -> str:
    import json

    # First, read the JSON data
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
    except FileNotFoundError:
        jsondata = {"folder_dirs": {},"values":{}}
    
    def longfind():
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

# def findval(valuename:str) -> str:
#     import json

#     # First, read the JSON data
#     try:
#         with open(JSON_PATH, 'r') as j:
#             jsondata = json.load(j)
#     except FileNotFoundError:
#         # Create default structure if file doesn't exist
#         jsondata = {"folder_dirs": {},"values":{}}
#         print("No folder with the given name")
#         return "CANT FIND JSON"

#     try:
#         return jsondata['values'][valuename]
#     except KeyError:
#         print(f"The value {valuename} doesn't exist in 'values'")
#         return "DOES NOT EXIST"
#         # from common.common import askstring
#         # jsondata['values'][valuename] = askstring(msg="Provide the value for this key:")
#         # with open("common/data.json", 'w') as j:
#         #     json.dump(jsondata,j)

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

def dropdown(choices: list[str], title='', icon_path=None) -> str: 
    """Create a wxPython window with a dropdown menu and return the selected item on Enter or OK button."""
    
    app = wx.App(False)  # Create the wx.App instance

    # Create a frame (main window)
    frame = wx.Frame(None, title=title, size=(315, 150))
    
    # Set custom icon if provided
    if icon_path:
        try:
            icon = wx.Icon(icon_path, wx.BITMAP_TYPE_ICO)  # For .ico files
            frame.SetIcon(icon)
        except Exception as e:
            print(f"Failed to load icon: {e}")
    
    # Center the frame on the screen
    frame.CenterOnScreen()
    
    # Rest of your existing code remains the same...
    panel = wx.Panel(frame)
    
    dropdown = wx.Choice(panel, choices=choices, pos=(50, 20), size=(200, -1))
    dropdown.SetSelection(0)
    
    selected_item = [None]
    
    button_width = 70
    button_spacing = 10
    total_button_width = (button_width * 2) + button_spacing
    start_x = (300 - total_button_width) // 2
    
    ok_button = wx.Button(panel, label="OK", pos=(start_x, 70), size=(button_width, 30))
    cancel_button = wx.Button(panel, label="Cancel", pos=(start_x + button_width + button_spacing, 70), size=(button_width, 30))
    
    def on_key_press(event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            selected_item[0] = dropdown.GetString(dropdown.GetSelection())
            print(f"Selected item: {selected_item[0]}")
            frame.Close()
        else:
            event.Skip()
    
    def on_ok(event):
        selected_item[0] = dropdown.GetString(dropdown.GetSelection())
        print(f"Selected item: {selected_item[0]}")
        frame.Close()
    
    def on_cancel(event):
        selected_item[0] = None
        print("Selection cancelled")
        frame.Close()
    
    frame.Bind(wx.EVT_CHAR_HOOK, on_key_press)
    ok_button.Bind(wx.EVT_BUTTON, on_ok)
    cancel_button.Bind(wx.EVT_BUTTON, on_cancel)
    
    frame.Show()
    app.MainLoop()
    
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

def remove_other(stringinput:str) -> str:
    """
    Cleans a *`string`* to remove characters that arent **PERIODS** or **NUMBERS**
    """
    clean_string = ""
    for char in stringinput:
        if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
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
    return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folders(dir:str) -> list[str]:
    return [folder for folder in os.listdir(dir) if os.path.isdir(os.path.join(dir, folder))]

def unhide_folder(dir:str):
    import sys,subprocess
    creationflags = 0
    if sys.platform == 'win32':
        creationflags = subprocess.CREATE_NO_WINDOW
                
    subprocess.run(['attrib', '-h', dir], check=True, creationflags=creationflags)

def is_date(date_string):
    from datetime import datetime
    """Simple date checker for most common formats"""
    common_formats = ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']
    
    for fmt in common_formats:
        try:
            datetime.strptime(date_string.strip(), fmt)
            return True
        except ValueError:
            continue
    return False