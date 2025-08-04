import os
import re
import wx
from common.common import windowpath,find_folder_path,is_dir
def rename_folders(folder_path=None):
    for content in os.listdir(folder_path):
        if os.path.isdir(content) and content != ".git":
            if "(" in content:
                os.rename(content,content.split("(")[0])
            else:
                try:
                    # Count items in the directory
                    item_count = len([item for item in os.listdir(content) if os.path.isfile(os.path.join(content, item))])
                    
                    # Check if folder name already has a count pattern (e.g., "folder (5)")
                    count_pattern = r'\s*\(\d+\)$'
                    match = re.search(count_pattern, content)
                    
                    if match:
                        # Extract the current count from the folder name
                        current_count_str = re.search(r'\((\d+)\)', content).group(1)
                        current_count = int(current_count_str)
                        
                        # Only rename if the count has changed
                        if current_count != item_count:
                            # Remove the old count pattern and add the new one
                            base_name = re.sub(count_pattern, '', content)
                            new_name = f"{base_name} ({item_count})"
                            try:
                                os.rename(content, new_name)
                                print(f"Updated '{content}' to '{new_name}' (count changed from {current_count} to {item_count})")
                            except OSError as e:
                                print(f"Error renaming '{content}': {e}")
                        else:
                            print(f"Skipped '{content}' - count is already correct ({item_count})")
                    else:
                        # No count pattern exists, add one
                        new_name = f"{content} ({item_count})"
                        try:
                            os.rename(content, new_name)
                            print(f"Added count to '{content}' -> '{new_name}'")
                        except OSError as e:
                            print(f"Error renaming '{content}': {e}")
                            
                except (OSError, PermissionError) as e:
                    print(f"Error accessing directory '{content}': {e}")

import os
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
            except PermissionError:
                content_count[content] = "Access Denied"
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

def main():
    startpath = windowpath()
    if is_dir(startpath):
        show_content(startpath)
    else:
        path = find_folder_path(startpath)
        show_content(path)

if __name__ == "__main__":
    #show_content()
    main()