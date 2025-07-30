import shutil
import sys
import os,pyperclip
if len(sys.argv) > 1:
    path_arg = sys.argv[1]
    # Check if the argument is a valid directory path
    if os.path.isdir(path_arg):
        tomove = path_arg
    else:
        # If not a full path, try to construct one from common locations
        possible_paths = [
            os.path.join(os.path.expanduser("~"), path_arg),      # User folder
            os.path.join(os.path.expanduser("~"), "Desktop", path_arg), # Desktop
            os.path.join("C:\\", path_arg)                       # Root drive
        ]
        for path in possible_paths:
            if os.path.isdir(path):
                tomove = path
                break

src = pyperclip.paste().strip("\"")
shutil.move(src,tomove)

