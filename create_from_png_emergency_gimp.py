import os
from common.common import *
from process_folders import emergency_overlay_maker 

for file in list_filespaths(r"C:\Users\samahalabo\Desktop\.SNAPSHOTS (images)"):
    basename = os.path.basename(file)
    cage_number = basename.split("-")[0]
    date = basename.split("-")[1]
    emergency_overlay_maker(cage_numbers=[cage_number], date=date, pngpath=file,room="OPTO-ROOM (12 cages)")