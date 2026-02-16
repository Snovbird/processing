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


def step1_organize_recordings_DATASAVE():
    last_step = findval("salvage_processing_step")
    if "step1_organize_recordings_DATASAVE" not in last_step:
        return step2_create_folders_and_move()

    recording_folderpath = findval("salvage_processing_step")["step1_organize_recordings_DATASAVE"]["recordings_folder"]
    grouped_recordings = findval("salvage_processing_step")["step1_organize_recordings_DATASAVE"]["grouped_recordings"]
    {'20251103': [['01-20251103-104708-113000.mp4', '01-20251103-113000-114505.mp4','03-20251103-104708-113000.mp4'], #exp1
                  ['01-20251103-122945-130000.mp4', '01-20251103-130000-133000.mp4']], #experiment 2
    '20251104': [['01-20251104-093838-100000.mp4', '01-20251104-100000-103000.mp4'], 
                 ['01-20251104-112135-120000.mp4', '01-20251104-120000-122642.mp4']]}

    override_first_cue = findval("salvage_processing_step")["step1_organize_recordings_DATASAVE"]["override_first_cue"]

    folders_to_create = []
    for date_number, (date,experiment_groups) in enumerate(grouped_recordings.items()): # unpack dates
        
        date_folderpath = makefolderpath(os.path.dirname(recording_folderpath), foldername=date, start_at_1=False)

        folders_to_create.append({"date_folderpath": date_folderpath,"experiment_folders":[],"grouped_experiments":[]})
        
        grid_rownames = []
        for experiment_number,videos_per_experiment in enumerate(experiment_groups,start=1): #make question string
            first = videos_per_experiment[0]
            time_start = first.split("-")[2]
            hour = time_start[0:2]
            minute = time_start[2:4]
            row_name_question = f"Experiment #{experiment_number} at {hour}:{minute}"
            grid_rownames.append(row_name_question)
            
        if not override_first_cue:
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each experiment (row names)
                                                    options_list=["DS+","DS-","SEEKING_TEST"], # options for each row
                                    title="First Cue",
                                    message=f"Select the first cue illuminated in experiments on {date}"
                                    )
            answer = list(answer_dict.values())
        else: 
            answer_dict:dict[str,str] = grid_selector(strings_list=grid_rownames, #time for each experiment (row names)
                                                    options_list=["YES","NO"], # options for each row
                                    title="Merge wrongly separated experiments",
                                    message=f"Are these separate experiments on {date}"
                                    )
            answer = list(answer_dict.values())

            for i, ans in enumerate(answer):
                if ans == "NO":
                    experiment_groups[i-1].extend(experiment_groups[i])
                    experiment_groups[i-1].sort()
                    del experiment_groups[i]

            answer = ["SEEKING_TEST"] * len(experiment_groups)

        for experiment_number, first_DS in enumerate(answer, start=0): 
            # first_DS is either DS+, DS- or SEEKING_TEST

            folder_name = makefolderpath(f"{date}_{experiment_number} {first_DS}", start_at_1=False)

            folders_to_create[date_number]["experiment_folders"].append(folder_name)
            folders_to_create[date_number]["grouped_experiments"].append((experiment_groups[experiment_number]))

        print(f"{folders_to_create=}")

        assignval("salvage_processing_step", {"step2_create_folders_and_move":{
            "recordings_folderpath": recording_folderpath,
            "folders_to_create": folders_to_create,
            "grouped_recordings": grouped_recordings}})
        

def step2_create_folders_and_move(dict_saved_step1):

    last_step = findval("salvage_processing_step")
    if "step2_create_folders_and_move" not in last_step:
        return step3

    recording_folderpath = dict_saved_step1["step2_create_folders_and_move"]["recordings_folderpath"]
    folders_to_create = dict_saved_step1["step2_create_folders_and_move"]["folders_to_create"]
    grouped_recordings = dict_saved_step1["step2_create_folders_and_move"]["grouped_recordings"]
    RECORDINGS_PATH = find_folder_path("0-RECORDINGS")
    dict_saved_step1["moved"] = dict_saved_step1.get("moved",[])



    if False:
        for date, exp_number_and_info in folders_to_create.items():
            date_folder = makefolder(RECORDINGS_PATH, date,start_at_1=False)

            for experiment_number, experiment_info in exp_number_and_info.items():
                experiments, first_DS = experiment_info
                experiment_folder = makefolder(date_folder, f"{date}_{experiment_number} {first_DS}", start_at_1=False)



                for experiment in experiments:
                    video_path = os.path.join(recording_folderpath, experiment)
                    dst = experiment_folder
                    shutil.move(video_path, dst)


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


def step3():
    pass

def continuous_process():
    recordings_folder = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))

    if not findval("salvage_processing_step"):

        override_first_cue = custom_dialog("Separate each video into DS+/DS- intervals (for training only)", title="Specify first cue")
        if not override_first_cue:
            return
        
        grouped_recordings = group_by_date_and_experimentTime(recordings_folder,max_pause=750,warn_for_lost_time=True)

        assignval("salvage_processing_step", {"step1_organize_recordings_DATASAVE": 
                                              {"recordings_folder": recordings_folder, 
                                               "grouped_recordings": grouped_recordings,
                                               "override_first_cue": override_first_cue}})
        
        step1_organize_recordings_DATASAVE()
    else:
        last_command = list(findval("salvage_processing_step").keys())[0]
        exec(f"{last_command}()")