from common.common import *
import os, shutil,time
from cagename import name_cages
from concatenate import concatenate, group_files_by_digits
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng
from markersquick import apply_png_overlay,find_imgpath_overlay_date
from newtrim import trim_DS_auto
def group_by_date_and_experimentTime(videos_folderpath: str) -> dict[str, list[list[str]]]:
    """
    Returns:
        {
            20250122: [
                ['1a-20250122-1300-1400.mp4','1b-20250122-1400-1500.mp4',...], # Experiment 1
                ['10a.-20250122-1500-1617.mp4',...] # Experiment 2
            ],
            20250123:[ [...],[...]]
        }
    """
    recordings = list_files(videos_folderpath)
    grouped_recordings = {}
    starts = []
    for recording in recordings: # group by date
        # 7a-20251122-120000-130000.mp4
        date = recording.split('-')[1]
        cage = recording.split('-')[0]
        cage = "".join([i for i in cage if i.isdigit()]) # keep only digits from cage string
        grouped_recordings[date] = grouped_recordings.get(date, {})
        grouped_recordings[date][cage] = grouped_recordings[date].get(cage, [])
        grouped_recordings[date][cage].append(recording)
    
    for date in grouped_recordings:
        exp_groups:dict[int, list[str]] = {}
        for cage in grouped_recordings[date]:
            cage_exp_groups = []
            cage_exp_group = []
            last_endtime = None
            for video_number, recording in enumerate(grouped_recordings[date][cage]):
                experiment_starttime = recording.split('-')[2]
                hours = int(experiment_starttime[:2])
                minutes = int(experiment_starttime[2:4])
                seconds = int(experiment_starttime[4:6]) + minutes*60 + hours *3600
                if not last_endtime: # first recording for the cage
                    cage_exp_group.append(recording)
                elif seconds - last_endtime <= 5: # technically supposed to be identical end & start times, but allow for small variations
                    cage_exp_group.append(recording)
                else: # other experiment started
                    cage_exp_groups.append(cage_exp_group)
                    cage_exp_group = [recording]

                if video_number == len(grouped_recordings[date][cage]) - 1:
                    cage_exp_groups.append(cage_exp_group) # append last group

                experiment_endtime = recording.split('-')[3]
                hours = int(experiment_endtime[:2])
                minutes = int(experiment_endtime[2:4])
                last_endtime = int(experiment_endtime[4:6]) + minutes*60 + hours*3600

            for number, exp_group in enumerate(cage_exp_groups):
                exp_groups[number] = exp_groups.get(number, []) + exp_group
        
        grouped_recordings[date] = exp_groups.values()

    return grouped_recordings,starts
    
class process_recordings():
    def __init__(self, recording_folderpath):
        self.recording_folderpath = recording_folderpath
        self.grouped_recordings = None
        self.experiment_folders = []
        self.processes_folder:dict[str, str] = {}
        self.first_DS_or_Interval = ["DS+","DS-","SEEKING_TEST"]
        
        overlays_path = find_folder_path("2-MARKERS")
        room_options = list_folders(overlays_path)
        self.room = dropdown(room_options + ["ENTER NEW ROOM NAME"],title="Select lab test room",icon_name="star",hide=("MARKERS-TEMPLATES",))
        if self.room == "ENTER NEW ROOM NAME":
            return emergency_overlay_maker()

        self.final_outputpath = find_folder_path("3-PROCESSED")      
        try:
            name_cages(self.recording_folderpath)
        except: #already named
            pass
    

    def step1_organize_recordings(self):
        self.grouped_recordings = group_by_date_and_experimentTime(self.recording_folderpath)
        for date,experiments in self.grouped_recordings.items():
            date_folder = makefolder(self.recording_folderpath, date,start_at_1=False)

            questions = {}
            keys = {}
            for count,experiments_list in enumerate(experiments):
                first = experiments_list[0]
                time_start = first.split("-")[2]
                hour = time_start[0:2]
                minute = time_start[2:4]
                row_name = f"Experiment #{count+1} at {hour}:{minute}"
                keys[row_name] = count
                questions[experiments_list] = row_name
            
            
            answer:dict[str,str] = grid_selector(questions.values(),self.first_DS_or_Interval,
                                   "First Cue",
                                   f"Select the first cue illuminated in experiments on {date}"
                                   )
            
            interpret_answer = {}
            for question, first in answer.items():
                count = keys[question]
                experiment = experiments[count]
                interpret_answer[experiment] = first

            for count, (experiment, first) in enumerate(interpret_answer.items()):
                experiment_folder = makefolder(date_folder, f"{date}_{count+1} {first}", start_at_1=False)
                self.experiment_folders.append(experiment_folder)
        
        for date, experiments in self.grouped_recordings.values():
            folders = list_folderspaths(
                    os.path.join(self.recording_folderpath, date)
                )

            for experiment_number, experiment_list in enumerate(experiments):
                for video in experiment_list:
                    video_path = os.path.join(self.recording_folderpath, video)
                    dst = folders[experiment_number]
                    shutil.move(video_path, dst)
        else:
            if os.listdir(self.recording_folderpath) == []:
                msgbox(f"This path is empty and will be deleted:\n{self.recording_folderpath}")
            else:
                error("Error deleting the recordings_folderpath. Opening:")
                os.startfile(self.recording_folderpath)
            # sleep(1)
            # os.rmdir(self.recording_folderpath)

    def step2_photo_carrousel(self):
        photos_folders = {}
        photos_to_carrousel = []
        for experiment_folder in self.experiment_folders:
            photos_folders[experiment_folder] = makefolder(experiment_folder, "photos", start_at_1=False)

        for count, (experiment_folder, photos_folder) in enumerate(photos_folders.items()):
                
            for cage_group in group_files_by_digits(list_filespaths(experiment_folder)):

                first_video = cage_group[0]

                photos_to_carrousel.append(
                    extractpng(first_video,times=[1],output_folder=photos_folder)[0] # use string not tuple (default output)              
                )
        
        combinedpaths = {}
        for photopath in photos_to_carrousel:
            basename = os.path.splitext(os.path.basename(photopath))[0]
            cage_string, date, *_ = basename.split("-")
            cage_number = "".join([i for i in cage_string if i.isdigit()])
            overlay = find_imgpath_overlay_date(date,room=self.room,cage_number=cage_number)

            outpath = os.path.dirname(photopath)

            combinedpaths[photopath] = combine_and_resize_images(photo1_path=photopath,
                                          photo2_path=overlay,
                                          output_folder=outpath)
            
        # photo carrousel; find disaligned markers
        for photopath,img in combinedpaths.items(): 
            if photo_carrousel(img) == "STOP markers NOT aligned":
                # find original video
                basename = os.path.splitext(os.path.basename(photopath))[0]
                cage_string, date, *_ = basename.split("-")
                cage_number = "".join([i for i in cage_string if i.isdigit()])
                parent = os.path.dirname(os.path.dirname(img)) # Experiment folder > photos > combined20.png
                for video in list_filespaths(parent):
                    vid_basename = os.path.splitext(os.path.basename(video))[0]
                    if vid_basename == basename:
                        break # found
                else:
                    error(f"No matching video file found for {basename}")
                    return
                
                return emergency_overlay_maker(cage_numbers=[cage_number],room=self.room,date=date,videos=[vid_basename])
        
        return self.step3_concatenate_videos()


    def step3_concatenate_videos(self):
        todelete = None
        for experiment_folder in self.experiment_folders:
            videos = list_filespaths(experiment_folder)
            
            if len(videos) == 0:
                continue
            
            grouped_videos = group_files_by_digits(videos)

            for group in grouped_videos:
                concatenate(group,experiment_folder)
            for video in todelete:
                if os.path.exists(video):
                    try:
                        os.remove(video)
                    except:
                        pass
            if todelete:
                attempt_delete(todelete)
            todelete = videos
        print("Files organized\n\nStarting concatenation...")

        count = 0
        while todelete: # last cage group cleanup
            for video in todelete:
                    if os.path.exists(video):
                        try:
                            os.remove(video)
                            todelete.remove(video)
                        except:
                            time.sleep(1)
                            count += 1
                            print(f"error deleting file, try #{count}")
        print("Concatenation and clean up complete")
    
    def step4_TrimIntervals(self):

        for experiment in self.experiment_folders:
            DS_cue = experiment.split(" ")[-1]
            videos = list_filespaths(experiment)
            trim_DS_auto(videos,first="DS_Cue",interval_duration=90,batch_size=5)

    def step5_markers(self):
        marker_folders = []
        for experiment in self.experiment_folders:
            basename = os.path.basename(experiment)
            marked = makefolder(experiment,basename,start_at_1=False)
            marker_folders.append(marked)
            
            for concat_vid in list_filespaths(experiment):
                basename = os.path.splitext(os.path.basename(concat_vid))[0]

                number, date, *_ = basename.split("-")

                apply_png_overlay(concat_vid,marked,self.room)

        for folder in marker_folders:
            shutil.move(folder,self.final_outputpath)


def emergency_overlay_maker(cage_numbers:list[str]=None,room=None,date=None,videos=None):
    marker_overlays_path = find_folder_path("2-MARKERS")
    if not date:
        date = askstring("Please enter the date as YYYYMMDD for this overlay. \nDefault is today's date.",fill=get_date_yyyymmdd())
    if not room:
        room = dropdown(list_folders(marker_overlays_path) + ["ENTER NEW ROOM NAME"],title="Select lab test room",icon_name="star",hide=("MARKERS-TEMPLATES",))
        
    room_folder_path = os.path.join(marker_overlays_path,room)
    if not cage_numbers:
        cage_numbers:list[int] = [ askint("Enter the cage number:","Cage number") ]
        if not cage_numbers:
            return
    if not videos:
        msgbox("A file explorer window will open next. From the explorer, select a video from which an image will be extracted to align the markers.\nThis image will be automatically added to the opened folder.")
        videos:str = select_video("Select video from which an image will be extracted. It will be used to align the markers")
        if not videos:
            return
    msgbox(f"emergency {videos=}\n\n{cage_numbers=}\n\n{room=}\n\n{date=}")
    for video,cage_number in zip(videos,cage_numbers):
        if not room: # 2-MARKERS/ NEWROOMNAME /
            room = askstring("Provide the name of the new room:","New room name",fill="ROOMNAME (numberofcages)")
            project_folderpath = makefolder(marker_overlays_path,foldername=room,start_at_1=False)
        else: # 2-MARKERS/OPTO-ROOM/cage2_20250806/
            project_folderpath = makefolder(room_folder_path,f"cage{cage_number}-{date}",start_at_1=False)
        
        unnamed_project_folderpath = shutil.copy(os.path.join(find_folder_path("MARKERS-TEMPLATES"),"template.xcf"),project_folderpath)
        renamed_project_path = os.path.join(project_folderpath,f"cage{cage_number}-{date}.xcf")
        os.rename(unnamed_project_folderpath,renamed_project_path)
        times = 1
        imgpath = extractpng(video=video,times=(times,),output_folder=room_folder_path)[0]
        
        # while photo_carrousel(imgpath,"OK. All cue lights are lit.","NO. Jump 5s to find all 4 cue lights ON") !="OK. All cue lights are lit.":
        #     os.remove(imgpath)
        #     times += 5
        #     imgpath = extractpng(video=select_video("Select video from which an image will be extracted. It will be used to align the markers"),times=(times,),output_folder=room_folder_path)[0]
        
        dates:list[str] = findval("dates")
        if date not in dates:
            dates.append(date)
            assignval("dates",dates)

    os.startfile(room_folder_path)
         

if __name__ == "__main__":
    pass