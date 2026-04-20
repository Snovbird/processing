from common.common import *
import os, shutil,time
from cagename import name_cages
from concatenate import concatenate, group_files_by_digits
from photo_carrousel import photo_carrousel
from image_combine import combine_and_resize_images
from extractpng import extractpng
from markersquick import apply_png_overlay,find_overlay_path
from newtrim import trim_DS_auto
def group_by_date_and_sessionTime(videos_folderpath: str,max_pause=15,warn_for_lost_time=False) -> dict[str, list[list[str]]]:
    """
    Args:
        videos_folderpath: path to folder containing videos (possibly) over multiple days and containing multiple sessions per day
        max_pause: max number of seconds allowed between 2 video parts part of a same session. If more: considered a separate session
    Returns:
        {
            20250122: [
                ['1a-20250122-1300-1400.mp4','1b-20250122-1400-1500.mp4',...], # session 1
                ['10a.-20250122-1500-1617.mp4',...] # session 2
            ],
            20250123:[ [...],[...]]
        }
    """
    recordings = list_files(videos_folderpath)
    grouped_recordings = {}
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
            first = True
            for video_number, recording in enumerate(grouped_recordings[date][cage]):
                session_starttime = recording.split('-')[2]
                hours = int(session_starttime[:2])
                minutes = int(session_starttime[2:4])
                seconds = int(session_starttime[4:6]) + minutes*60 + hours *3600
                if not last_endtime: # first recording for the cage
                    cage_exp_group.append(recording)
                    if first:
                        first = False
                elif seconds - last_endtime == 0:
                    cage_exp_group.append(recording)
                elif seconds - last_endtime < max_pause: # technically supposed to be identical end & start times, but allow for small variations
                    if warn_for_lost_time:
                        error(f"""Note: {seconds - last_endtime} seconds have been lost between\n
                              {format_time_colons(str(last_endtime))} and {format_time_colons(str(session_starttime))}\n
                              for cage {cage} on the date (YYYYMMDD): {date}\n
                              ""","Warning")
                    "f".format()
                    cage_exp_group.append(recording)
                    if first:
                        first = False
                else: # other session started
                    cage_exp_groups.append(cage_exp_group)
                    cage_exp_group = [recording]
                    first = True


                if video_number == len(grouped_recordings[date][cage]) - 1:
                    cage_exp_groups.append(cage_exp_group) # append last group

                session_endtime = recording.split('-')[3]
                hours = int(session_endtime[:2])
                minutes = int(session_endtime[2:4])
                last_endtime = int(session_endtime[4:6]) + minutes*60 + hours*3600

            for number, exp_group in enumerate(cage_exp_groups):
                exp_groups[number] = exp_groups.get(number, []) + exp_group
        
        grouped_recordings[date] = list(exp_groups.values())


    return grouped_recordings
    
class process_recordings():
    def __init__(self, recording_folderpath):
        self.recording_folderpath = recording_folderpath
        self.grouped_recordings = None
        self.session_folders = []
        self.processes_folder:dict[str, str] = {}
        self.first_DS_or_Interval = ["DS+","DS-","SEEKING_TEST"]
        self.date_folders = []
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

    def start(self):
        self.step1_organize_recordings()

    def step1_organize_recordings(self):
        self.grouped_recordings = group_by_date_and_sessionTime(self.recording_folderpath)

        for date,sessions in self.grouped_recordings.items(): # unpack dates
            date_folder = makefolder(os.path.dirname(self.recording_folderpath), date,start_at_1=False)
            self.date_folders.append(date_folder)

            grid_rownames = []
            for session_number,sessions_list in enumerate(sessions,start=1):
                first = sessions_list[0]
                time_start = first.split("-")[2]
                hour = time_start[0:2]
                minute = time_start[2:4]
                row_name_question = f"session #{session_number} at {hour}:{minute}"
                grid_rownames.append(row_name_question)
            
            answer:dict[str,str] = grid_selector(grid_rownames,self.first_DS_or_Interval,
                                   "First Cue",
                                   f"Select the first cue illuminated in sessions on {date}"
                                   )
            
            for session_number, first_DS in enumerate(answer.values(),start=1): 
                session_folder = makefolder(date_folder, f"{date}_{session_number} {first_DS}", start_at_1=False)
                self.session_folders.append(session_folder)


        for date_folder, sessions in zip(self.date_folders,self.grouped_recordings.values()):
            folders = list_folderspaths(date_folder)

            for session_number, session_list in enumerate(sessions):
                for video in session_list:
                    video_path = os.path.join(self.recording_folderpath, video)
                    dst = folders[session_number]
                    shutil.move(video_path, dst)
        else:
            time.sleep(1)
            os.rmdir(self.recording_folderpath)

        return self.step2_photo_carrousel()
        
    def step2_photo_carrousel(self,session_fol = None):
        photos_folders = {}
        photos_to_carrousel = []
        if session_fol:
            self.session_folders = [session_fol]
        for session_folder in self.session_folders:
            photos_folders[session_folder] = makefolder(session_folder, "photos", start_at_1=False)

        for session_folder, photos_folder in photos_folders.items():
                
            for cage_group in group_files_by_digits(list_filespaths(session_folder)):

                first_video = cage_group[0]

                photos_to_carrousel.append(
                    screenshot(first_video,frame_number=0,
                    output_path=os.path.join(photos_folder, 
                                             os.path.basename(first_video).replace(".mp4", ".png"))
                        )
                    )              
                
        
        combinedpaths = {}
        for photopath in photos_to_carrousel:
            basename = os.path.splitext(os.path.basename(photopath))[0]
            cage_string, date, *_ = basename.split("-")
            cage_number = "".join([i for i in cage_string if i.isdigit()])
            overlay = find_overlay_path(date,room=self.room,cage_number=cage_number)

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
                parent = os.path.dirname(img) # session folder > photos 
                for video in list_filespaths(parent):
                    vid_basename = os.path.splitext(os.path.basename(video))[0]
                    if vid_basename == basename:
                        problematic_videopath = os.path.join(parent,video)
                        break # found
                else:
                    error(f"No matching video file found for {basename} in {parent}\nPurpose: extract png to make new overlay")
                    return
                
                return emergency_overlay_maker(cage_numbers=[cage_number],room=self.room,date=date,videos=[problematic_videopath])
        for folder in photos_folders.values():
            shutil.rmtree(folder)

        return self.step3_concatenate_videos()

    def step3_concatenate_videos(self):
        videos_to_delete = []  # Store original videos that should be deleted
        print("Files organized\n\nStarting concatenation...")
        
        for session_folder in self.session_folders:
            videos = list_filespaths(session_folder)
            print(f"{videos}\n\n{session_folder=}")
            if len(videos) == 0:
                continue
            
            grouped_videos = group_files_by_digits(videos)
            videos_to_delete.append([])
            
            for group in grouped_videos:
                concatenate(group, session_folder) # if singleitem, it will only be renamed to ##-YYYYMMDD.mp4

                if len(group) > 1: # single item = no concatenation = no deletion
                    videos_to_delete[-1].extend(group)

        # Delete only the original videos that were concatenated
        for original_vids in videos_to_delete:
            if not original_vids: #only one item in "group" = empty list --> no deletion needed
                continue

            for vid in original_vids:
                try:
                    os.remove(vid)
                    print(f"Deleted original video: {os.path.basename(vid)}")
                except Exception as e:
                    error(f"Error deleting {vid}\n\nError: {e}")
                
        return self.step4_TrimIntervals()
    
    def step4_TrimIntervals(self):

        for session in self.session_folders:
            DS_cue = session.split(" ")[-1]
            videos = list_filespaths(session)
            trim_DS_auto(videos,first=DS_cue,start_time=16,interval_duration=90,batch_size=5)

        return self.step5_markers()
    
    def step5_markers(self):
        marker_folders = []
        for session in self.session_folders:
            basename = os.path.basename(session)
            marked = makefolder(session,basename,start_at_1=False)
            marker_folders.append(marked)
            
            for concat_vid in list_filespaths(session):
                basename = os.path.splitext(os.path.basename(concat_vid))[0]

                apply_png_overlay(concat_vid,marked,self.room)

        for folder in marker_folders:
            shutil.move(folder,self.final_outputpath)

def emergency_overlay_maker(path,room=None):
    """
    Creates a gimp project 

    path: path to a png image or mp4 video. Creates a copy of the png inside the gimp folder, and takes a screenshot if a video is provided. Formatted as NN-YYYYMMDD-HHMMSS (rest is ignored)
    room: name of the room to put the overlay in. If None, will ask for it
    """
    marker_overlays_path = find_folder_path("2-MARKERS")

    if not room:
        room = dropdown(list_folders(marker_overlays_path) + ["ENTER NEW ROOM NAME"],title="Select lab test room",icon_name="star",hide=("MARKERS-TEMPLATES",))
        if room == "ENTER NEW ROOM NAME":
            room = askstring("Enter the room name:","Room name")
            room_folder_path = makefolder(marker_overlays_path,room,start_at_1=False)
        else:
            room_folder_path = os.path.join(marker_overlays_path,room)
    
    cage_number, date, *rest = os.path.splitext(os.path.basename(path))[0].split("-")        
    if rest:
        start_time = rest[0]
    else:
        start_time = None

         # 2-MARKERS/OPTO-ROOM/cage2_20250806/

    project_name = f"{cage_number.zfill(2)}-{date}" + f"-{start_time}" if start_time else ""
    project_folderpath = makefolder(room_folder_path,project_name,start_at_1=False)
    
    template_project_path = shutil.copy(os.path.join(find_folder_path("MARKERS-TEMPLATES"),"template.xcf"),project_folderpath)
    renamed_project_path = os.path.join(project_folderpath,f"{project_name}.xcf")
    os.rename(template_project_path,renamed_project_path)

    if path.endswith(".mp4"):
        screenshot(video_path=path,frame_number=0,output_path=os.path.join(project_folderpath,f"{project_name}.png"))
    elif path.endswith(".png"):
        shutil.copy(path,project_folderpath)
        new_path = os.path.join(project_folderpath,os.path.basename(path))
        os.rename(new_path,os.path.join(project_folderpath,f"{project_name}.png"))
        
    
    # while photo_carrousel(imgpath,"OK. All cue lights are lit.","NO. Jump 5s to find all 4 cue lights ON") !="OK. All cue lights are lit.":
    #     os.remove(imgpath)
    #     times += 5
    #     imgpath = extractpng(video=select_video("Select video from which an image will be extracted. It will be used to align the markers"),times=(times,),output_folder=room_folder_path)[0]
        
    os.startfile(project_folderpath)
         
def main():
    recordings_folder = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))
    process_recordings(recordings_folder).start()

if __name__ == "__main__":
    main()