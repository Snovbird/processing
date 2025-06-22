import os
from common.common import select_folder,windowpath,askstring,custom_dialog
import shutil
def main():
    startpath = windowpath()
    folder_path = select_folder(title="Select FOLDER to delete files inside",path=startpath)

    stringtodelete = askstring("Search for keyword:")
    # ifincluded = custom_dialog(msg="Only delete if this string is INCLUDED or EXCLUDED?",title="File name handling",op1='INCLUDED',op2='EXCLUDED')
    
    for i in os.listdir(folder_path):
        if len(i.split('_')) > 2:
            os.remove(os.path.join(folder_path,i))
        if stringtodelete in i and False:
            os.remove(os.path.join(folder_path,i))

main()