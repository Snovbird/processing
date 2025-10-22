import time,shutil,os
from common.common import clear_gpu_memory,assignval,findval,find_folder_path,msgbox,list_folderspaths
from TRIM import trim_frames
while True:
    time.sleep(4)
    queue:list = findval("trim_queue")
    if queue:
        first_item:dict = queue.pop(0)
        if first_item.get("done"):
            for i in list_folderspaths(os.path.dirname(first_item["input_path"])):
                if "done" in i.lower():
                    donepath = i
            shutil.move(first_item["input_path"],donepath)
            assignval("trim_queue",queue)
            continue
        # pyperclip.copy(f"""path = {first_item["input_path"]}\nstart_time = {first_item["start_time"]}\nend_time = {first_item["end_time"]}""")
        assignval("trim_queue",queue)
        outpath = first_item.get("output_path",find_folder_path("5-clips"))
        trim_frames(first_item["input_path"],first_item["start_time"],int(first_item["end_time"])+1,outpath,show_terminal=False)
        clear_gpu_memory()
        
        # 1. Get the current 'trim_done' data.
        trim_done_data = findval("trim_done")
        
        # 2. If it's not a dictionary (e.g., first run or invalid data), initialize it.
        if not isinstance(trim_done_data, dict):
            trim_done_data:dict = dict()

        # 3. Get the existing string of trims for this path, if any.
        existing_trims:str = trim_done_data.get(first_item["input_path"], None)

        # 4. Create a list of all parts to join (old and new).
        parts_to_join:list = [existing_trims] if existing_trims else []
        parts_to_join.extend([first_item["start_time"], first_item["end_time"]])

        # 5. Join them with a period and update the dictionary.
        trim_done_data[first_item["input_path"]] = ".".join(parts_to_join)
        assignval("trim_done", trim_done_data)
    else:
        time.sleep(5)