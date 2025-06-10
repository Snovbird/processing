
import os
import wx
def renamefromfolder(folderpath,file):
    name, extension = os.path.splitext(file)
    os.rename(os.path.join(folderpath,file),os.path.join(folderpath,os.path.basename(os.path.dirname(folderpath)) + extension)
def select_folder(message="Choose a directory containing files:"):
    """Show folder selection dialog and return selected path"""
    with wx.DirDialog(None, message, 
                      style=wx.DD_DEFAULT_STYLE) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            folder_path = dlg.GetPath()
            return folder_path
        return None
    
def main():
    app = wx.App(False)

    selectedfolder = select_folder()
    for file in os.listdir(selectedfolder):
        if os.path.isfile(file):

if __name__ == "__main__":
    main()