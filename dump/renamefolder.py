
import os
import wx
def rename_file_to_folder_name(folderpath,file,count = 0):
    name, extension = os.path.splitext(file)
    newfilepath = os.path.join(folderpath,os.path.basename(os.path.dirname(folderpath)) + count.replace('0','')+ extension)
    if os.path.exists(newfilepath):
        count +=1
        rename_file_to_folder_name(folderpath,file,count)
    os.rename(os.path.join(folderpath,file),newfilepath)

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
            rename_file_to_folder_name(selectedfolder,file)
if __name__ == "__main__":
    main()