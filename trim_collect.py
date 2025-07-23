import pyperclip,os
from common.common import askstring,remove_other,assignval,findval
import subprocess
vid = pyperclip.paste().strip("\"")

file,ext = os.path.splitext(os.path.basename(vid))
os.startfile(os.path.join(
    os.path.dirname(vid),
    'overlaid1',
    f'{file}-overlaid{ext}'
    ))
both_times:list = remove_other(askstring("start_times and end_times separated by a period:")).split(".")
start_times:list = [both_times[i] for i in range(0,len(both_times),2)]
end_times:list = [both_times[i] for i in range(1,len(both_times),2)]

assignval("trim_queue",[{"input_path":vid,"start_time":start_times[i],"end_time":end_times[i]} for i in range(len(start_times))])
# subprocess.run(["pythonw",__file__])

