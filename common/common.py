# no need to import modules present in __init__ (will be run first) # NOT SURE ABOUT THAT ACTUALLY
import wx
import os
import subprocess
# answer = CustomDialog(None, title="", message="", option1="", option2="")

def windowpath():
    import win32gui
    window = win32gui.GetForegroundWindow()
    print(type(win32gui.GetWindowText(window)))
    return win32gui.GetWindowText(window).replace(' - File Explorer','')

def custom_dialog(title,msg,op1,op2):

    class custom_dialog(wx.Dialog):
        def __init__(self, parent, title, message, option1="Proceed", option2="Skip"):
            super().__init__(parent, title=title, size=(300, 150), style=wx.DEFAULT_DIALOG_STYLE)
            
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

def select_folder(title="Choose a directory",chosenpath=''):
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
    if chosenpath:
        try:
            with wx.DirDialog(None, title, defaultPath=chosenpath,style=wx.DD_DEFAULT_STYLE) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    folder_path = dlg.GetPath()
                    return folder_path
        except:
            return pathDNE()
    else:
        return pathDNE()

def clear_gpu_memory():
    try:
        # Reset GPU clocks temporarily to help clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False
    
def select_video(title="Select videos",chosenpath=''):
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
    if chosenpath:
        try:
            with wx.FileDialog(
                None,
                message=title,
                defaultDir=chosenpath,
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

def select_anyfile(title="Select files",chosenpath=''):
    # Create wildcard string for video files
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
    if chosenpath:
        try:
            with wx.FileDialog(
                None,
                message=title,
                defaultDir=chosenpath,
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

def askint(title="Integer Input",question="Enter an integer:",fill=''):
    """Open a dialog to ask for an integer, pre-filled with 10."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, question, title, value='0')
    
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        try:
            result = int(dlg.GetValue())  # Convert the input to an integer
            print(f"Entered integer: {result}")
            return result
        except ValueError:
            wx.MessageBox("Invalid input. Please enter a valid integer.", "Error", wx.ICON_ERROR)
    dlg.Destroy()  # Clean up the dialog
    return None

def askstring(title="String Input",question="Enter a string:",fill=''):
    """Open a dialog to ask for a string, pre-filled with 'abcde123'."""
    app = wx.App(False)  # Create the wx.App instance
    dlg = wx.TextEntryDialog(None, question, title, value=f'{fill}')
    
    if dlg.ShowModal() == wx.ID_OK:  # If the user clicks OK
        result = dlg.GetValue()  # Get the entered string
        print(f"Entered string: {result}")
        return result
    dlg.Destroy()  # Clean up the dialog
    return None

def makefolder(file_path, foldername='',count=1):
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


