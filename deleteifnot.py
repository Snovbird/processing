import os
from common.common import select_folder,windowpath,askstring

def delete_files(folder_path,stringtodelete):
    for i in os.listdir(folder_path):
        currentfile = os.path.join(folder_path,i)
        if len(i.split('_')) > 2 and os.path.isfile(currentfile):
            os.remove(currentfile)
        if stringtodelete in i and False:
            os.remove(os.path.join(folder_path,i))

def main():
    startpath = windowpath()
    folder_path = select_folder(title="Select FOLDER to delete files inside",path=startpath)

    stringtodelete = askstring("Search for keyword:")
    # ifincluded = custom_dialog(msg="Only delete if this string is INCLUDED or EXCLUDED?",title="File name handling",op1='INCLUDED',op2='EXCLUDED')
    delete_files(folder_path,stringtodelete)

if __name__ == "__main__":
    main()