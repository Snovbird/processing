from common.common import *
import os, shutil,time
from cagename import name_cages
from concatenate import concatenate, group_files_by_digits
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng
from markersquick import apply_png_overlay,find_imgpath_overlay_date
from newtrim import trim_DS_auto
from process_folders import group_by_date_and_experimentTime

first_DS_or_Interval = ["DS+","DS-","SEEKING_TEST"]

def step1_organize_recordings(recording_folderpath, override_first_cue=None):
    grouped_recordings = group_by_date_and_experimentTime(recording_folderpath)
    date_folders = []
    experiment_folders = []
    for date,experiments in grouped_recordings.items(): # unpack dates
        date_folder = makefolder(os.path.dirname(recording_folderpath), date,start_at_1=False)
        date_folders.append(date_folder)

        grid_rownames = []
        for experiment_number,experiments_list in enumerate(experiments,start=1):
            first = experiments_list[0]
            time_start = first.split("-")[2]
            hour = time_start[0:2]
            minute = time_start[2:4]
            row_name_question = f"Experiment #{experiment_number} at {hour}:{minute}"
            grid_rownames.append(row_name_question)
        
        answer:dict[str,str] = grid_selector(grid_rownames,first_DS_or_Interval,
                                "First Cue",
                                f"Select the first cue illuminated in experiments on {date}"
                                )
        
        for experiment_number, first_DS in enumerate(answer.values(),start=1): 
            experiment_folder = makefolder(date_folder, f"{date}_{experiment_number} {first_DS}", start_at_1=False)
            experiment_folders.append(experiment_folder)


    for date_folder, experiments in zip(date_folders,grouped_recordings.values()):
        folders = list_folderspaths(date_folder)

        for experiment_number, experiment_list in enumerate(experiments):
            for video in experiment_list:
                video_path = os.path.join(recording_folderpath, video)
                dst = folders[experiment_number]
                shutil.move(video_path, dst)
    else:
        time.sleep(1)
        os.rmdir(recording_folderpath)

    return step2_photo_carrousel()


def continuous_process():
    recordings_folder = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))

    if not findval("salvage_processing_step"):

        step1_organize_recordings(recordings_folder)