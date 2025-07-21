pathtosort = r"C:\Users\samahalabo\Videos\0-RECORDINGS\2025-7-17"

import os
import shutil
for date in ['20250714','20250715','20250716','20250717']:
    os.makedirs(os.path.join(pathtosort,date))
    for file in [os.path.join(pathtosort,f) for f in os.listdir(pathtosort) if os.path.isfile(os.path.join(pathtosort,f))]:
        if date in file:
            shutil.move(file,os.path.join(pathtosort,date))
