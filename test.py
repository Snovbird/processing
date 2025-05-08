# for letter in ["a",'b','c']:
#     for i in [1,2,3,4,5,6]:
#         if i == 3:
#             break
#         else:
#             print(letter,i)


# video_paths = ("C:/apple.mp4/","C:/oranges.mp4")
# width = 1024
# for vid in video_paths:
#     if not askforcage:
#         for i in range(12):
#             if len(str(12-i)) == 2 and str(12-i) in vid.split("/")[-2]:
#                     output_path = print(vid, i+1, width)
#                     break
#             elif str(12-i) in vid.split("/")[-2]: 
#                 output_path = apply_png_overlay(vid, 12-i, width)
#     elif askforcage:
#         output_path = print(vid, cage_number, width)

# import tkinter as tk
# from tkinter import filedialog, messagebox
# import os
# import subprocess
# import platform
# from tkinter import simpledialog
# a = filedialog.askopenfilename()
# print(a.split("/")[-1].replace(".mp4",""),a.split("/")[-2].replace(".mp4",""))

file_paths = ('a','b','c')
for i, path in enumerate(file_paths):
    if i > 0:
        # Clear GPU memory between files
        print('not first')
    print(i, path)
