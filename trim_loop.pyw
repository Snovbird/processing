import time
from common.common import clear_gpu_memory,assignval,findval
from TRIM import trim_frames
while True:
    time.sleep(4)
    queue:list = findval("trim_queue")
    if queue:
        first_item:dict = queue.pop(0)
        assignval("trim_queue",queue)

        trim_frames(first_item["input_path"],first_item["start_time"],first_item["end_time"],r"C:\Users\samahalabo\Desktop\behavior clips",show_terminal=False)
        clear_gpu_memory()
    else:
        time.sleep(5)