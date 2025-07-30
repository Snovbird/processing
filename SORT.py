# The unused imports from common.common and os have been removed for clarity.
import wx
import os
import win32gui
import win32process
import psutil
import shutil
import win32com.client

parent_path = r"C:\Users\samahalabo\Desktop\5-behavior video CLIPS"
sorted_folders = {
    folder_name[0].lower() : os.path.join(parent_path,folder_name) for folder_name in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path,folder_name))
}

def main():
    # wx.App(False) means stderr/stdout are not redirected to a wx window.
    app = wx.App(False)
    
    # Create a small, borderless frame. It will be almost invisible, but it is
    # necessary to have a frame to capture key events with this method.
    frame = wx.Frame(None, title="Key Press Listener", size=(1, 1))
                    #  style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)

    # The original UI elements are removed as the window is not meant to be visible.
    # The output will go to the console.

    def on_key_down(event):
        keycode = event.GetKeyCode()
        # In modern wxPython (4+), key constants like wx.WXK_A are deprecated.
        # We can compare against the ASCII values of uppercase letters directly.
        # The keycode for letters is the uppercase ASCII value.
        if ord('A') <= keycode <= ord('Z'):
            key_char = chr(keycode).lower()
            print(f"Key Pressed: {key_char}")
            # Close the app after a key is pressed.
            # Use CallAfter to safely close from an event handler.
            # wx.CallAfter(frame.Close)
        # add code here after importing libraries
            if key_char in sorted_folders:
                # Get the currently active window
                hwnd = win32gui.GetForegroundWindow()
                
                # Get the process ID of the active window
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                
                # Get the process object
                process = psutil.Process(pid)
                
                # Check if the process is explorer.exe
                if process.name().lower() == "explorer.exe":
                    # Get the path of the active Explorer window
                    shell = win32com.client.Dispatch("Shell.Application")
                    for window in shell.Windows():
                        if window.HWND == hwnd:
                            current_explorer_path = window.Document.Folder.Self.Path
                            break
                    else:
                        current_explorer_path = None

                    if current_explorer_path and os.path.isdir(current_explorer_path):
                        # Get all selected files/folders in the current Explorer window
                        selected_items = []
                        for item in window.Document.SelectedItems():
                            selected_items.append(item.Path)
                        
                        if selected_items:
                            destination_folder = sorted_folders[key_char]
                            for item_path in selected_items:
                                try:
                                    # Move the item
                                    shutil.move(item_path, destination_folder)
                                    print(f"Moved '{os.path.basename(item_path)}' to '{destination_folder}'")
                                except Exception as e:
                                    print(f"Error moving '{item_path}': {e}")
                            # Refresh the explorer window
                            shell.RedrawWindow()
                        else:
                            print("No items selected in Explorer.")
                    else:
                        print("Active window is not an Explorer window or path not found.")
                else:
                    print("Active window is not Explorer.exe")
            else:
                print(f"No sorted folder configured for key '{key_char}'")

        # Allow other handlers to process the event.
        # event.Skip()

    frame.Bind(wx.EVT_CHAR_HOOK, on_key_down)
    
    # We must show the frame and give it focus to receive key events.
    # Even though it's tiny, it needs to be shown.
    frame.Show(True)
    
    print("Listening for a single alphabetical key press (a-z)...")
    
    app.MainLoop()

if __name__ == "__main__":
    main()
