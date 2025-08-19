import os
import wx
# Get the absolute path to the directory containing this file (common.py)
COMMON_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_PATH = os.path.dirname(COMMON_CURRENT_DIR)
# Define the path to data.json, assuming it's in the same directory as this script.
# This makes file access independent of where the script is run from.
JSON_PATH = os.path.join(COMMON_CURRENT_DIR, 'data.json')

# no need to import modules present in __init__ (will be run first) # NOT SURE ABOUT THAT ACTUALLY
# answer = CustomDialog(None, title="", message="", option1="", option2="")


def custom_dialog(msg="",title='',op1="yes",op2="No",op3=None,dimensions:tuple[int,int] = (300, 150)) -> str:

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

def askint(msg:str="Enter an integer:", title:str="Integer Input", fill:str|int=0) -> int:
    
    
    """Open a dialog to ask for an integer, always on top."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, msg, title, value=f"{fill}", style=wx.OK | wx.CANCEL)
    dlg.Centre()
    
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        try:
            result = int(dlg.GetValue())  # Convert the input to an integer
            dlg.Destroy()
            app.Destroy()
            return result
        except ValueError:
            dlg.Destroy()
            error(f"{fill} is not a valid default value. Please enter a valid integer.")
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
        new_folder_name = f"{foldername.replace('-','')}-{count}"

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

def msgbox(msg:str,title:str=' '):
    

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(f"{msg}", f"{title}", wx.OK | wx.ICON_INFORMATION)

def error(msg:str,title:str="ERROR"):
    

    app = wx.App(False)  # Create the wx.App instance

    wx.MessageBox(f"Error: {msg}", f"{title}", wx.OK | wx.ICON_ERROR)

def wrap(text_input:str,text_to_wrap:str) -> str:
    '''
    To a *`string`*: appends on both sides of a 'text_input' another string 'text_to_wrap'
    '''
    return f"{text_to_wrap}{text_input}{text_to_wrap}"

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

def list_files(dir:str) -> list[str]:
    """
    returns:
    the NAMES of files in a directory

    ex: `apples.mp4,banana.mp4`
    """
    return [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]

def list_folders(dir:str) -> list[str]:
    """
    returns:
    the NAMES of folders in a directory

    ex: `apples,banana`
    """
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