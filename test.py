from common.common import assignval

import wx
app = wx.App(False)  # Create the wx.App instance
import os
    
parent_path = r"C:\Users\samahalabo\Desktop\5-behavior video CLIPS"
sorted_folders = {folder_name[0].lower():os.path.join(parent_path,folder_name) for folder_name in os.listdir(parent_path) if os.path.isdir(os.path.join(parent_path,folder_name))
}
print(sorted_folders)
