import pyperclip,os
from common.common import askstring,remove_other,assignval,findval,error,is_file
import subprocess

def trim_collect(vid:str,pss_string:str,true=None):

    print(vid)
    if not is_file(vid): # if is not a path althogether: the error should terminate the script
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
        if not true:
            true = pss_string
        both_times:list = pss_string.split(".")
        pss_string:str = remove_other(askstring("start_times and end_times separated by a period:",f"{os.path.basename(vid)}",fill=true)).strip(".")
        if not pss_string:
            return
        start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
        end_times:list = [both_times[i] for i in range(1,len(both_times),2)]

    print(start_times,end_times)
    assignval("trim_queue",[{"input_path":vid,"start_time":start_times[i],"end_time":end_times[i]} for i in range(len(start_times))])
    
def main():
    vid = pyperclip.paste().strip( '"' )
    if not is_file(vid):
        error(f"Not a file:\n{vid}")
        return
    while True:
        pss_string:str = remove_other(askstring("start_times and end_times separated by a period:",f"{os.path.basename(vid)}")).strip(".")
        if not pss_string:
            return
        trim_collect(vid,adjust(pss_string),pss_string)

def add_done_to_queue():
    to_trim = findval("trim_done")
    for vid,pss_string in to_trim.items():
        trim_collect(vid,adjust(pss_string))

def adjust(pss_string:str) -> str:
    both_times:list = pss_string.split(".")
    for c, time in enumerate(both_times):
        if time == both_times[c-1]:
            both_times[c-1] = f'{int(both_times[c-1])-1}'
    return ".".join(both_times)

if __name__ == "__main__":
    
    if False: # add manually
        
        path = None 

        pss_string = None

        trim_collect(vid,adjust(pss_string))
        both_times:list = pss_string.split(".")
    else:
        main()
