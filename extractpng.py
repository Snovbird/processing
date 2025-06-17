import subprocess
import os
from common.common import clear_gpu_memory,select_video,askstring
import wx

def extractpng(video,times):
    selectedtimes = []
    for seconds in times:
        selectedtimes.append(f"eq(t,{seconds})")
    
    selectedtimes = "+".join(selectedtimes)
    cmd = ['ffmpeg', 
           '-hwaccel', 'cuda', 
           '-hwaccel_output_format', 'cuda',
            '-c:v', 'h264_cuvid', 
            '-i', 'input.mp4', 
            '-vf', f'select=\'{selectedtimes}\',hwdownload,format=nv12',
            '-vsync', '0', 
            '-q:v', '1', 
            'frame_%02d.png']
    subprocess.run(cmd, check=True)


def toseconds(timestring):
    for timestr in timestring.split('.'):

        time_input = time_input.strip()
        
        if time_input.isdigit():
            time_input = time_input.zfill(6)
            return int(time_input[:-4])*3600 + int(time_input[-4:-2])*60 + int(time_input[-2:])
def main():
    videos = select_video(title="Videos to extract frames from")
    times = askstring(title='Times','')
    for video in videos:
        extractpng
    os.startfile(os.path.dirname(videos[0]))
    




if __name__ == '__main__':
    main()
