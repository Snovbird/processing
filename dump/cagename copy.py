import os
import wx
import win32gui
import win32process
import win32com.client
import psutil
import sys
    
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
def get_explorer_path():
    """Get the current path of an active Explorer window"""
    hwnd = win32gui.GetForegroundWindow()
    if is_explorer_window(hwnd):
        # Use Shell.Application to get the Explorer window and its path
        shell = win32com.client.Dispatch("Shell.Application")
        windows = shell.Windows()

        for window in windows:
            try:
                if window.HWND() == hwnd:
                    return window.Document.Folder.Self.Path
            except:
                continue
    
    return None

def is_explorer_window(hwnd):
    """Check if the window is a File Explorer window"""
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        # print('p:',process.name().lower())
        # with open(r"C:\Users\Labo Samaha\Downloads\nothing.txt",'a') as test:
        #     test.write(process.name().lower())
        if process.name().lower() == "explorer.exe":
            class_name = win32gui.GetClassName(hwnd)
            if class_name == "CabinetWClass" or class_name == "ExploreWClass":
                return True
    except Exception as e:
        print(str(e))
    return False

def select_folder():
    """Show folder selection dialog and return selected path"""
    with wx.DirDialog(None, "Choose a directory containing files:", 
                      style=wx.DD_DEFAULT_STYLE) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            return folder_path
        return None

def get_string_input(question,title):
    """Show text input dialog for string"""
    with wx.TextEntryDialog(None, question,title) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            input_string = dlg.GetValue().strip()
            if not input_string:
                wx.MessageBox("Please enter a valid string!", "Warning", 
                              wx.OK | wx.ICON_WARNING)
                return None
                
            # Remove invalid filename characters
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                input_string = input_string.replace(char, '')
            return input_string
        return None

def process_files(source_folder):
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
    source_folder = get_explorer_path()
    if not source_folder:
        source_folder = select_folder()
    if not source_folder:
        return
        
    # Step 3: Process files
    try:
        process_files(source_folder)
    except Exception as e:
        wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


if __name__ == "__main__":
    main()
