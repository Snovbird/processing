from common.common import *
import os, shutil
from frameoverlay import overlay_FRAMES
def find_done_folder(path = find_folder_path("5-clips"),DS = "DS-"):
    collectedpath = os.path.join(path,f"collected {DS}")
    for folderpath in list_folderspaths(collectedpath):
        if "done" in folderpath:
            return folderpath
    

def rename_done_folder(path = find_folder_path("5-clips"),DS = "DS-"):
    collectedpath = os.path.join(path,f"collected {DS}")
    original_clipspath = os.path.join(collectedpath,"originals")
    original_clips = list_files(original_clipspath)
    for folderpath in list_folderspaths(collectedpath):
        if "done" in folderpath:
            donepath = folderpath
            break
    
    newname = f"done ({len(list_files(donepath))} of {len(original_clips)})"
    
    shutil.move(donepath,os.path.join(collectedpath,newname))

def clips_overlay_missing(path = find_folder_path("5-clips"),DS = "DS-"):
    collectedpath:str = os.path.join(path,f"collected {DS}")
    original_clips:list = list_files(os.path.join(collectedpath,"originals"))

    currently_overlaid = [i.replace("-overlaid","") for i in list_files(collectedpath)]

    donepath:str = find_done_folder(path,DS)
    done_files:list = list_files(donepath)
    for i in original_clips:
        if i not in currently_overlaid and i not in done_files:
            overlay_FRAMES(os.path.join(collectedpath,"originals",i),collectedpath,append_to_name="")

if __name__ == "__main__":
    rename_done_folder()
    clips_overlay_missing()