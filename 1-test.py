import pandas,os,wx,pyperclip
from common.common import *
import timeit
from process_folders import group_by_date_and_experimentTime
a = select_folder()

r = group_by_date_and_experimentTime(a)

# Assuming 'r' is a dictionary like:
# r = {
#     '2023-01-01': ['itemA', 'itemB'],
#     '2023-01-02': ['itemC', 'itemD']
# }

# Original code with syntax error
# readable = f'{"\n\n".join[f"{date}:\n{", ".join(items)}" for date, items in r.items()]}'

# Corrected and more readable version
readable = "\n\n".join(
    f"{date}:\n{', '.join(map(str, items))}" for date, items in r.items()
)
msgbox(readable)