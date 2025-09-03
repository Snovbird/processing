import os
from common.common import find_folder_path,custom_dialog,list_folders,dropdown,msgbox
def main():
    clipspath = find_folder_path("5-clips")

    choice = dropdown(list_folders(clipspath),"Select folders for which cue?")
    if not choice:
        return
    dir6 = find_folder_path("6-GENERATED EXAMPLES")
    count = 0
    for folder in [folder for folder in os.listdir(os.path.join(clipspath,choice)) if os.path.isdir(os.path.join(clipspath,choice, folder))]:
        
        if folder != "no idea":
            os.makedirs(os.path.join(dir6,folder),exist_ok=True)
            count += 1
    msgbox(f"{count} folders created","Success")

main()