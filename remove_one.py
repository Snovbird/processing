import keyboard
import pyperclip
from TRIM import trim_frames

from common.common import get_duration
import os
def send_ctrl_shift_c():
    """Sends the key combination Ctrl + Shift + C."""
    keyboard.press_and_release('ctrl+shift+c')

def main():

    fullpath = pyperclip.paste().strip("\"")

    fullname = os.path.splitext(os.path.basename(fullpath))[0]
    filename, timestamps = fullname.split("-trim(")
    filename += os.path.splitext(os.path.basename(fullpath))[1]
    print(filename,timestamps)
    start,end = timestamps.strip(")").split("-")
    end = int(end) - 2
    original_path = os.path.join(r"C:\Users\samahalabo\Desktop\collected DS+\overlaid1\old",filename[0],filename)
    output_path = trim_frames(original_path,start,end,output_folder=r"C:\Users\samahalabo\Desktop\5-behavior video CLIPS",show_terminal=False)
    # os.remove(fullpath)
        # os.rename(output_path,fullpath)

if __name__ == "__main__":
    main()
