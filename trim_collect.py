import pyperclip,os
from common.common import *

def trim_collect(vid:str,pss_string:str,true=None):
    if findval("which_DS") == False:
        cue = custom_dialog(msg="Select cue", title="Cue folder", op1="DS-", op2="DS+")
        if not cue:
            return
        assignval("which_DS", cue)
    print(vid)
    if not is_file(vid): # if is not a path althogether: the error should terminate the script
        return

    both_times:list = pss_string.split(".")

    if len(both_times) == 2: # 10.20
        which_DS = findval("which_DS")
        start_time:str = both_times[0]
        end_time:str = both_times[1]
        while not int(start_time) < int(end_time):
            error("Start time must be before end time")
            pss_string:str = remove_other(askstring("Try again. Start_time and end_time separated by a period:",f"{os.path.basename(vid)} (T)",fill=pss_string)).strip(".")
            if not pss_string:
                finish = custom_dialog("Mark this interval video as done?",title=f"{vid} (T)")
                if finish == "yes":
                    assignval("trim_done",{"input_path":vid,"done":True})
                return 
            both_times:list = pss_string.split(".")
            start_time:str = both_times[0]
            end_time:str = both_times[1]
        clipspath = find_folder_path("5-clips")

        full_behavior_names = list_folders(os.path.join(clipspath,which_DS))
        # shortened_names = [name.split(" ")[1] if len(name.split(" ")) > 1 else name for name in full_behavior_names]
        # behavior = full_behavior_names[simple_dropdown(shortened_names,"Select behavior name:","Behavior",return_index=True)]
        behavior = simple_dropdown(full_behavior_names,"Select behavior name:","Behavior")
        
        queue = findval("trim_queue")
        if not isinstance(queue, list): queue = []

        if behavior:
            outpath = os.path.join(clipspath,which_DS,behavior)
            queue.append({"input_path":vid,"start_time":start_time,"end_time":end_time,"output_path":outpath})
        else: #closed window
            queue.append({"input_path":vid,"start_time":start_time,"end_time":end_time})
        assignval("trim_queue",queue)
    else: # 100.300.400.500...
        start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
        end_times:list = [both_times[i] for i in range(1,len(both_times),2)]

        while len(start_times) != len(end_times):
            error("Provide same number of start and end times")
            if not true:
                true = pss_string
            pss_string:str = remove_other(askstring("start_times and end_times separated by a period:",f"{os.path.basename(vid)}",fill=true)).strip(".")
            both_times:list = pss_string.split(".")
            if not pss_string:
                return
            start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
            end_times:list = [both_times[i] for i in range(1,len(both_times),2)]     
            

        print(start_times,end_times)
        
        queue = findval("trim_queue")
        if not isinstance(queue, list): queue = []
        queue.extend([{"input_path":vid,"start_time":start_times[i],"end_time":end_times[i]} for i in range(len(start_times))])
        assignval("trim_queue",queue)
    
def main():
    vid = pyperclip.paste().strip( '"' )
    if not is_file(vid):
        error(f"Not a file:\n{vid}")
        return
    if findval("which_DS") == False:
        cue = custom_dialog(msg="Select cue", title="Cue folder (T)", op1="DS-", op2="DS+")
        if not cue:
            return
        assignval("which_DS", cue)

    while True:
        raw_pss_string:str = askstring("start_times and end_times separated by a period:",title=f"{os.path.basename(vid)} (T)")
        if not raw_pss_string:
            finish = custom_dialog("Mark this interval video as done?",title=f"{vid} (T)")
            if finish == "yes":
                queue = findval("trim_queue")
                queue.append({"input_path":vid,"done":True})
                assignval("trim_queue",queue)
            return
        pss_string:str = remove_other(raw_pss_string).strip(".")
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
