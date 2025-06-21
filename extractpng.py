import subprocess
import os
from common.common import clear_gpu_memory,select_video,askstring,makefolder,windowpath

def extractpng(video, times):
    selectedtimes = []
    subfolder = makefolder(video,'png')
    
    # Add a 0.05 second tolerance to each timestamp
    tolerance = 0.05
    for seconds in times:
        selectedtimes.append(f"between(t,{seconds-tolerance},{seconds+tolerance})")
    
    select_filter_with_tolerance = "+".join(selectedtimes)
    
    cmd = ['ffmpeg', 
           '-hwaccel', 'cuda', 
           '-hwaccel_output_format', 'cuda',
           '-c:v', 'h264_cuvid', 
           '-i', video, 
           '-vf', f"select='{select_filter_with_tolerance}',hwdownload,format=nv12",
           '-vsync', '0', 
           '-q:v', '1', 
           os.path.join(subfolder, 'frame_%02d.png')]
    
    subprocess.run(cmd, check=True)


def toseconds(timestring):
    secondslist = []
    for timestr in timestring.split('.'):

        time_input = timestr.strip()
        
        if time_input.isdigit():
            time_input = time_input.zfill(6)
            secondslist.append(int(time_input[:-4])*3600 + int(time_input[-4:-2])*60 + int(time_input[-2:]))
    return secondslist

def main():
    
    start = windowpath()
    videos = select_video(title="Videos to extract frames from",path=start)

    if not videos:
        return
    times = toseconds(askstring(title='Times',msg="Enter HHMMSS times separated by a period (.):"))
    if not times:
        return

    for video in videos:
        extractpng(video,times)
    clear_gpu_memory()
    os.startfile(os.path.dirname(videos[0]))
    

if __name__ == '__main__':
    main()
