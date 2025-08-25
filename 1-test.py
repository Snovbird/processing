import pandas,os
from common.common import assignval,list_folders,list_folderspaths,makefolder,simple_file_walk,msgbox,select_video
def main():
    a = []
    while True:
        choice = [f"'{i.replace('\\','/')}'" for i in select_video()]
        if not choice:
            break
        a.append(choice)
    import pyperclip
    pyperclip.copy(a)
main()