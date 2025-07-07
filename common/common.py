import os

# Get the absolute path to the directory containing this file (common.py)
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to data.json, assuming it's in the same directory as this script.
# This makes file access independent of where the script is run from.
JSON_PATH = os.path.join(_CURRENT_DIR, 'data.json')

# no need to import modules present in __init__ (will be run first) # NOT SURE ABOUT THAT ACTUALLY
# answer = CustomDialog(None, title="", message="", option1="", option2="")

def windowpath() -> str:
    import win32gui
    window = win32gui.GetForegroundWindow()
    return str(win32gui.GetWindowText(window)).replace(' - File Explorer','').replace("\\\\","/")

def custom_dialog(msg="",title='',op1="yes",op2="No",dimensions:tuple|int = (300, 150)) -> str:
    import wx

    class custom_dialog(wx.Dialog):
        def __init__(self, parent, title, message, option1="Proceed", option2="Skip"):
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

        app = wx.App(False)  # Create the wx.App instance
    
    app = wx.App()
    # Create the dialog
    dialog = custom_dialog(None, title=title, message=msg, option1=op1, option2=op2)
    
    # Show the dialog modally and get the result
    if dialog.ShowModal() == wx.ID_OK:
        dialog.Destroy()  # Clean up the dialog
        return dialog.result
    else:
        dialog.Destroy()  # Clean up the dialog
        return dialog.result

def select_folder(title="Choose a directory",path='') -> str:
    """Show folder selection dialog and return selected path"""
    import wx
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
    
def select_video(title="Select videos",path='') -> str:
    import wx
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
    wildcard = "Video Files (*.mp4)|*.mp4" #"Video files (*.mp4;*.avi)|*.mp4;*.avi" #"Video Files (*.mp4)|*.mp4" #"Video Files (*.mp4;*.avi;*.mov;*.mkv;*.webm)|*.mp4;*.avi;*.mov;*.mkv;*.webm"
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

def select_anyfile(title="Select files",path='') -> str:
    import wx
    app = wx.App(False)
    wildcard = "Any files (*.*)|*.*"
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

def askint(msg="Enter an integer:",title="Integer Input",fill='')  -> int:
    import wx

    """Open a dialog to ask for an integer, pre-filled with 10."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value='0', style=wx.OK | wx.STAY_ON_TOP)
    dlg.Centre()

    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        try:
            result = int(dlg.GetValue())  # Convert the input to an integer
            print(f"Entered integer: {result}")
            return result
        except ValueError:
            wx.MessageBox("Invalid input. Please enter a valid integer.", "Error", wx.ICON_ERROR)
    dlg.Destroy()  # Clean up the dialog
    return None

def askstring(msg="Enter a string:",title="String Input",fill='') -> str:
    import wx

    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=f'{fill}',style= wx.OK | wx.STAY_ON_TOP)
    dlg.Centre()
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        result = dlg.GetValue()  # Get the entered string
        print(f"Entered string: {result}")
        return result
    dlg.Destroy()  # Clean up the dialog
    return None

def makefolder(file_path, foldername='',count=1) -> str:
    import os
    # Get directory containing the file
    if os.path.isdir(file_path):
        folder_path = file_path
    else:
        folder_path = os.path.dirname(file_path)
        # file_name = os.path.splitext(os.path.basename(file_path))[0]    # Get just the filename without extension
    
    # Create folder name
    resized_folder_name = f"{foldername}{count}"
    
    # Create full path to new folder
    resized_folder_path = os.path.join(folder_path, resized_folder_name)
    # Check if folder exists and print debug info
    print(f"Checking if folder exists: {resized_folder_path}")
    print(f"Folder exists: {os.path.exists(resized_folder_path)}")
    
    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        # messagebox.showerror("ERROR", f"DELETE the folder {resized_folder_name}")
        # os.startfile(os.path.dirname(resized_folder_path))
        # return None
        return makefolder(file_path,foldername,count+1)
    else:
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
    return resized_folder_path

def get_duration(video_path) :
    import os
    import cv2
    import datetime
    """
    Get the duration of a video file
    
    Args:
        video_path: Path to the video file
        
    Returns:
        A tuple containing (seconds, formatted_time)
    """
    # Check if file exists
    if not os.path.isfile(video_path):
        print(f"Error: File '{video_path}' does not exist")
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
    seconds = round(frames / fps)
    
    # Format time as HH:MM:SS
    HHMMSS = str(datetime.timedelta(seconds=seconds)).replace(":","")
    
    # Release the video object
    video.release()
    
    return frames, seconds, HHMMSS

def msgbox(msg:str,title=''):
    import wx

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(msg, title, wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP)

def error(msg:str):
    import wx

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(f"Error: {msg}", "Error", wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)

def find_folder_path(foldername:str) -> str:
    import os
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
        print("No folder with the given name")
        return None

    try:
        findfolder = jsondata['folder_dirs'][foldername]
        if os.path.exists(findfolder):
            return findfolder
        else:
            return longfind()
    except KeyError:
        return longfind()
    
def findval(valuename:str) -> str:
    import json

    # First, read the JSON data
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
    except FileNotFoundError:
        # Create default structure if file doesn't exist
        jsondata = {"folder_dirs": {},"values":{}}
        print("No folder with the given name")
        return "CANT FIND JSON"

    try:
        print(jsondata['values'][valuename])
        return jsondata['values'][valuename]
    except KeyError:
        print(f"The value {valuename} doesn't exist in 'values'")
        return "DOES NOT EXIST"
        # from common.common import askstring
        # jsondata['values'][valuename] = askstring(msg="Provide the value for this key:")
        # with open("common/data.json", 'w') as j:
        #     json.dump(jsondata,j)

def assignval(valuename:str,value):
    import json
    try:
        with open(JSON_PATH, 'r') as j:
            jsondata = json.load(j)
        jsondata['values'][valuename] = value
        
        with open(JSON_PATH, 'w') as j:
            json.dump(jsondata,j,indent=4)
            print(f"Successfully assigned {value} to {valuename}!")
    except Exception as e:
        print(f"Failed to assign {value} to {valuename}.\nError: {e}")

def dropdown(choices: list[str],title='') -> str: 
    """Create a wxPython window with a dropdown menu and return the selected item on Enter."""
    import wx
    app = wx.App(False)  # Create the wx.App instance

    # Create a frame (main window)
    frame = wx.Frame(None, title=title, size=(300, 150))
    
    # Create a panel to hold the dropdown menu
    panel = wx.Panel(frame)
    
    # Create a dropdown menu (wx.Choice) with some options
    dropdown = wx.Choice(panel, choices=choices, pos=(50, 30), size=(200, -1))
    dropdown.SetSelection(0)  # Set the default selection to the first item
    
    # Variable to store the selected item
    selected_item = [None]  # Use a mutable object (list) to store the result
    
    # Event handler for pressing Enter
    def on_enter(event):
        selected_item[0] = dropdown.GetString(dropdown.GetSelection())  # Get the selected item
        print(f"Selected item: {selected_item[0]}")  # Print the selected item
        frame.Close()  # Close the window
    
    # Bind the Enter key to the event handler
    frame.Bind(wx.EVT_CHAR_HOOK, on_enter)
    
    # Show the frame
    frame.Show()
    app.MainLoop()
    
    # Return the selected item after the window is closed
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
    Append a given "text_to_wrap" string to another "text_input" string
    '''
    return f"{text_to_wrap}{text_input}{text_to_wrap}"


