import pyperclip,os
from common.common import askstring,remove_other,assignval,findval,error
import subprocess

def trim_collect(vid:str,pss_string:str):

    print(vid)
    if not os.path.isfile(vid): # if is not a path althogether: the error should terminate the script
        return
    # file,ext = os.path.splitext(os.path.basename(vid))
    # os.startfile(os.path.join(
    #     os.path.dirname(vid),
    #     'overlaid1',
    #     f'{file}-overlaid{ext}'
    #     ))

    # os.startfile(vid)
    both_times:list = pss_string.split(".")
    start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
    end_times:list = [both_times[i] for i in range(1,len(both_times),2)]

    while len(start_times) != len(end_times):
        error("Provide same number of start and end times")
        pss_string:str = remove_other(askstring("start_times and end_times separated by a period:",f"{os.path.basename(vid)}",fill=pss_string)).strip(".")
        if not pss_string:
            return
        both_times:list = pss_string.split(".")
        start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
        end_times:list = [both_times[i] for i in range(1,len(both_times),2)]


    print(start_times,end_times)
    assignval("trim_queue",[{"input_path":vid,"start_time":start_times[i],"end_time":end_times[i]} for i in range(len(start_times))])
    # subprocess.run(["pythonw",__file__])

def main():
    pss_string:str = remove_other(askstring("start_times and end_times separated by a period:",f"{os.path.basename(vid)}")).strip(".")
    if not pss_string:
        return
    vid = pyperclip.paste().strip("\"")
    trim_collect(vid,pss_string)

def add_done_to_queue():
    to_trim = findval("trim_done")
    for vid,pss_string in to_trim.items():
        trim_collect(vid,pss_string)

if __name__ == "__main__":
    main()