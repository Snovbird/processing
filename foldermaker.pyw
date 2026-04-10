import os
from common.common import *
def main():
    clipspath = find_folder_path("5-clips")

    choice = dropdown([folder for folder in list_folders(clipspath) if "." not in folder],"Select cue to create folders for")
    if not choice:
        return
    dir6 = find_folder_path("6-GENERATED EXAMPLES")
    count = 0
    for folder in [folder for folder in os.listdir(os.path.join(clipspath,choice)) if os.path.isdir(os.path.join(clipspath,choice, folder))]:
        
        if "." not in folder:
            os.makedirs(os.path.join(dir6,folder),exist_ok=True)
            count += 1
    msgbox(f"{count} folders created","Success")

main()