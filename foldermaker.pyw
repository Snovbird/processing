import os
from common.common import find_folder_path
clipspath = find_folder_path("5-clips")
for folder in [folder for folder in os.listdir(clipspath) if os.path.isdir(os.path.join(clipspath,folder))]:
    if folder != "no idea":
        os.makedirs(os.path.join(find_folder_path("6-GENERATED EXAMPLES"),folder),exist_ok=True)