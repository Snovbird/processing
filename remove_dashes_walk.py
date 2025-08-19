import os,shutil
from common.common import select_folder

def simple_file_walk_renamer(folder):
    """
    walks through all files in a folder
    """
    for root, dirs, files in os.walk(folder):
        for file in files:
            if "_" in file:
                newname = file.replace("_",'-')
                os.rename(os.path.join(root, file), os.path.join(root, newname))

# Usage

folder_path = select_folder("Enter folder path: ").strip().strip('"\'')
simple_file_walk_renamer(folder_path)














