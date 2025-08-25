import os
from common.common import find_folder_path,custom_dialog,list_folders
def main():
    clipspath = find_folder_path("5-clips")

    op1, op2, *_ = list_folders(clipspath)
    choice = custom_dialog("Select folders for which cue?","Cue","DS+","DS-")
    if not choice:
        return
    dir6 = find_folder_path("6-GENERATED EXAMPLES")
    for folder in [folder for folder in os.listdir(os.path.join(clipspath,choice)) if os.path.isdir(os.path.join(clipspath,choice, folder))]:
        if folder != "no idea":
            os.makedirs(os.path.join(dir6,folder),exist_ok=True)

main()