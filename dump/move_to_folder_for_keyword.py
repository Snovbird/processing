import wx,os

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

def main():
    
    # Get keyword from user
    keyword = wx.GetTextFromUser("Enter keyword to search for in filenames:", "Keyword Input")
    if not keyword:
        return
    
    # Get source folder
    source_folder = select_folder("Select folder containing files to move")
    if not source_folder:
        return
    
    # Get destination folder
    dest_folder = select_folder("Select destination folder")
    if not dest_folder:
        return
    
    # Find files containing the keyword
    matching_files = []
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        if os.path.isfile(file_path) and keyword.lower() in filename.lower():
            matching_files.append((filename, file_path))
    
    if not matching_files:
        wx.MessageBox(f"No files found containing keyword '{keyword}'", "No Files Found")
        return
    
    # Show confirmation dialog
    message = f"Found {len(matching_files)} files containing '{keyword}'.\nMove them to the destination folder?"
    if wx.MessageBox(message, "Confirm Move", wx.YES_NO | wx.ICON_QUESTION) != wx.YES:
        return
    
    # Move the files
    moved_count = 0
    for filename, source_path in matching_files:
        dest_path = os.path.join(dest_folder, filename)
        try:
            # Handle duplicate filenames
            counter = 1
            original_dest_path = dest_path
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(filename)
                dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext}")
                counter += 1
            
            os.rename(source_path, dest_path)
            moved_count += 1
        except Exception as e:
            wx.MessageBox(f"Error moving {filename}: {str(e)}", "Error")
    
    wx.MessageBox(f"Successfully moved {moved_count} files", "Complete")


if __name__ == "__main__":
    main()