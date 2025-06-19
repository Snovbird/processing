# pyperclip.copy('''ffmpeg -hwaccel cuda -hwaccel_output_format cuda -c:v h264_cuvid -i input.mp4 -vf "select='eq(t,30)+eq(t,60)+eq(t,90)+eq(t,120)+eq(t,150)',hwdownload,format=nv12" -vsync 0 -q:v 1 frame_%02d.png
# '''.split(' '))
# import sys
# import os
# import subprocess
# import pyperclip
# import wx

# import wx
# import os
# def select(chosenpath):
#     if os.path.isdir(chosenpath):
#         try:
#             with wx.FileDialog(
#                 None,
#                 message='title',
#                 defaultDir=str(chosenpath),
#                 wildcard="Video Files (*.mp4)|*.mp4",
#                 style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
#             ) as file_dialog:
                
#                 # Show the dialog and check if user clicked OK
#                 if file_dialog.ShowModal() == wx.ID_CANCEL:
#                     return []  # Return empty list if canceled
                    
#                 # Get the selected paths
#                 video_paths = file_dialog.GetPaths()
#                 return video_paths
#         except:
#             pass
            
# def windowpath():
#     import win32gui
#     window = win32gui.GetForegroundWindow()
#     print(type(win32gui.GetWindowText(window)))
#     return str(win32gui.GetWindowText(window)).replace(' - File Explorer','') #.replace("\\","\\\\")


# select(windowpath())

print('CONCATENATED_VID0.mp4'[16])