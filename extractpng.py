import subprocess
import os
from common.common import clear_gpu_memory,select_video,askstring,makefolder,windowpath
import wx

def extractpng(video,times,outputfolder):
    selectedtimes = []
    subfolder = makefolder(outputfolder,'png')
    for seconds in times:
        selectedtimes.append(f"eq(t,{seconds})")
    selectedtimes = "+".join(selectedtimes)
    cmd = ['ffmpeg', 
           '-hwaccel', 'cuda', 
           '-hwaccel_output_format', 'cuda',
            '-c:v', 'h264_cuvid', 
            '-i', video, 
            '-vf', f'select=\'{selectedtimes}\',hwdownload,format=nv12',
            '-vsync', '0', 
            '-q:v', '1', 
            os.path.join(subfolder,'frame_%02d.png')]
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
    try:
        start = windowpath()
        videos = select_video(title="Videos to extract frames from",chosenpath=start)
    except Exception as e:
        with open(r"C:\Users\samahalabo\Videos\Error.txt",'w') as file:
            file.write(str(e))
    if videos == None:
        return
    times = toseconds(askstring(title='Times',question="Enter HHMMSS times separated by a period (.):"))
    if times == None:
        return
    
    for video in videos:
        outputfolder = makefolder(os.path.basename())
        extractpng(video,times,outputfolder)
    clear_gpu_memory()
    os.startfile(os.path.dirname(videos[0]))
    




if __name__ == '__main__':
    main()
