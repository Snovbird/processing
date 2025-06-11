import tkinter as tk
import wx
import subprocess
import os

# answer = CustomDialog(None, title="", message="", option1="", option2="")
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

# def custom_dialog(title, message, option1="Proceed", option2="Skip"):
#     result = [False]  # Using a list to store the result
    
#     dialog = tk.Toplevel()
#     dialog.title(title)
#     dialog.geometry("300x150")
#     dialog.resizable(False, False)
#     dialog.grab_set()  # Make the dialog modal
#         # Center the dialog on the screen
#     dialog.update_idletasks()  # Update "requested size" from geometry manager
    
#     # Calculate position x, y
#     screen_width = dialog.winfo_screenwidth()
#     screen_height = dialog.winfo_screenheight()
#     dialog_width = dialog.winfo_width()
#     dialog_height = dialog.winfo_height()
    
#     position_x = int(screen_width/2 - dialog_width/2)
#     position_y = int(screen_height/2 - dialog_height/2)
    
#     # Position the window
#     dialog.geometry(f"+{position_x}+{position_y}")
    
#     # Create message label
#     label = tk.Label(dialog, text=message, wraplength=250, pady=20)
#     label.pack()
    
#     # Frame for buttons
#     button_frame = tk.Frame(dialog)
#     button_frame.pack(pady=10)
    
#     # Yes button with custom text
#     def on_op1():
#         result[0] = option1
#         dialog.destroy()
#     def on_op2():
#         result[0] = option2
#         dialog.destroy()
        
#     op1_button = tk.Button(button_frame, text=option1, width=8, command=on_op1)
#     op1_button.pack(side=tk.LEFT, padx=10)
    
#     # No button with custom text
#     op2_button = tk.Button(button_frame, text=option2, width=8, command=on_op2)
#     op2_button.pack(side=tk.LEFT, padx=10)
    
#     # Wait for the dialog to be closed
#     dialog.wait_window()
    
#     return result[0]

def select_folder():
    """Show folder selection dialog and return selected path"""
    with wx.DirDialog(None, "Choose a directory containing files:", 
                      style=wx.DD_DEFAULT_STYLE) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            return folder_path
        return None
    
def select_anyfile(msg="Select files"):
    """Show file selection dialog for any file type and return selected paths."""
    app = wx.App(False)  # Create a wx.App instance
    with wx.FileDialog(
        None,
        message=msg,
        wildcard="All files (*.*)|*.*",
        style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
    ) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()  # Get a list of selected file paths
            return paths
    return None

def select_video(msg="Select video files"):
    """Show file selection dialog for video files and return selected paths."""
    app = wx.App(False)  # Create a wx.App instance
    with wx.FileDialog(
        None,
        message=msg,
        wildcard="Video files (*.mp4;*.avi)|*.mp4;*.avi",
        style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST
    ) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()  # Get a list of selected file paths
            return paths
    return None

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
    




