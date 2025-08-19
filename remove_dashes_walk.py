import os,shutil
from common.common import select_folder,msgbox

def simple_file_walk_renamer(folder):
    """
    walks through all files in a folder
    """
    renamed = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            msgbox(file)
            if "_" in file:
                
                newname = file.replace("_",'-')
                os.rename(os.path.join(root, file), os.path.join(root, newname))
                renamed += 1
    return renamed

# Usage

folder_path = select_folder("Enter folder path: ").strip().strip('"\'')
c = simple_file_walk_renamer(folder_path)

msgbox(f"Renamed {c} files")














