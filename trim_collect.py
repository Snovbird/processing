import pyperclip
from common.common import askstring,remove_other
from TRIM import trim_frames
import subprocess
vid = pyperclip.paste().strip("\"")
output_folder = r"C:\Users\samahalabo\Desktop\behavior clips"


start_times = remove_other(askstring("start_times and end_times:")).split(".")
end_times = start_times.copy()[1:]

start_times = start_times.copy()[0:-1]

trim_frames(vid, start_times, end_times, output_folder=output_folder,show_terminal=False)

subprocess.run(["pythonw",__file__])

