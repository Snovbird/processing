import pyperclip
from TRIM import trim_frames

from common.common import get_duration,find_folder_path,error,msgbox
import os


def main():

    fullpath = pyperclip.paste().strip("\"")

    fullname = os.path.splitext(os.path.basename(fullpath))[0]
    filename, timestamps = fullname.split("-trim(")
    filename += os.path.splitext(os.path.basename(fullpath))[1]
    print(filename,timestamps)
    start,end,*_ = timestamps.strip(")").split("-")
    end = int(end) - 2
    original_path = os.path.join(r"C:\Users\samahalabo\Desktop\collected DS+\overlaid-1",filename)
    try:
        output_path = trim_frames(original_path,start,end,output_folder=find_folder_path("5-clips"),show_terminal=False)
        return output_path
    except Exception as e:
        error(f"Error: {e}\nCould not process: {fullpath}")
    # os.remove(fullpath)
        # os.rename(output_path,fullpath)

if __name__ == "__main__":
    main()
