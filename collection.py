import pyperclip
import os
import shutil

# Get the full content from the clipboard.
# If multiple files are copied, their paths are separated by newlines.

from common.common import error,findval,assignval

clipboard_content = pyperclip.paste().strip("\"")
paths = clipboard_content.splitlines()

if not paths:
    print("Clipboard is empty or does not contain a file path.")
else:
    # Per the request, get the last item from the clipboard
    path_to_move = paths[-1]

    new_folder = r"C:\Users\samahalabo\Desktop\collected DS+"

    # 1. Ensure the destination folder exists, create it if it doesn't
    os.makedirs(new_folder, exist_ok=True)

    # 2. Check if the source path from the clipboard is valid
    if os.path.exists(path_to_move):
        destination_path = os.path.join(new_folder, os.path.basename(path_to_move))
        # 3. Check if a file with the same name already exists to prevent overwriting
        count = 0
        while os.path.exists(destination_path):
            count += 1
            base_name = f"{os.path.splitext(os.path.basename(path_to_move))[0]}-{str(count).zfill(2)}{os.path.splitext(path_to_move)[1]}" # add a count to avoid overwriting of duplicate names
            destination_path = os.path.join(new_folder, base_name)
        # if os.path.exists(destination_path):
        #     # error(f"Skipping: '{os.path.basename(path_to_move)}' already exists in the destination.")
        #     new_folder = r"C:\Users\samahalabo\Desktop\collected DS+\collected 2"
        #     destination_path = os.path.join(new_folder, os.path.basename(path_to_move))
        else:
            # 4. Use the more robust shutil.move to move the file/folder
            shutil.move(path_to_move, new_folder)
            
    else:
        error(f"Error: The path '{path_to_move}' does not exist.")

