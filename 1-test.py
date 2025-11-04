import pandas,os,wx,pyperclip
from common.common import *
import timeit
from process_folders import group_by_date_and_experimentTime
def seegroups():
    a = select_folder()
    r = group_by_date_and_experimentTime(a)
    readable = "\n\n".join(
        f"{date}:\n{', '.join(map(str, items))}" for date, items in r.items()
    )
    msgbox(readable)
