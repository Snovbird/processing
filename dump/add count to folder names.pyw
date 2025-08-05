import os
import re
import wx

def show_content(folder_path=None):
    app = wx.App(False)
    
    content_count = {}
    
    # Only process directories, skip files
    for content in os.listdir(folder_path):
        if os.path.isdir(content):  # Check if it's a directory
            try:
                filecount = len([f for f in os.listdir(content) 
                               if os.path.isfile(os.path.join(content, f))])
                content_count[content] = filecount
            except Exception as e:
                content_count[content] = f"Error: {e}"
    
    if not content_count:
        wx.MessageBox("No directories found in current folder.", "No Directories", wx.OK | wx.ICON_INFORMATION)
        return
    
    # Create the message content
    message_lines = [f"{key} = {value}" for key, value in content_count.items()]
    total_files = sum(v for v in content_count.values() if isinstance(v, int))
    
    message = "Contents:\n" + '\n'.join(message_lines) + f"\nTOTAL: {total_files}"
    
    # Show ONE message box with all the information
    wx.MessageBox(message, "File Counts in each folder", wx.OK | wx.ICON_INFORMATION)


if __name__ == "__main__":
    show_content()