import os
from common.common import select_folder,windowpath,askstring,list_folderspaths,custom_dialog,list_files,msgbox

def delete_files(folder_path,stringtodelete):
    count = 0
    for i in list_files(folder_path):
        currentfile = os.path.join(folder_path,i)
        # if len(i.split('_')) > 2 and os.path.isfile(currentfile):
        #     os.remove(currentfile)
        if stringtodelete in i:
            os.remove(currentfile)
            count +=1
    return count

def main():
    startpath = windowpath()
    folder_path = select_folder(title="Select FOLDER to delete files inside",path=startpath)

    stringtodelete = askstring("Search for keyword:")
    # ifincluded = custom_dialog(msg="Only delete if this string is INCLUDED or EXCLUDED?",title="File name handling",op1='INCLUDED',op2='EXCLUDED')

    select = custom_dialog("select subfolder or same folder",'Delete in what',"subfolder","same folder")

    successes = []
    if select == "subfolder":
        for folder in list_folderspaths(folder_path):
            count:int = delete_files(folder,stringtodelete)
            successes.append(f"{count} files deleted from {os.path.basename(folder)}")
    elif select == "same folder":
        count:int = delete_files(folder_path,stringtodelete)
        successes.append(f"{count} files deleted from {folder_path}")

    msgbox("Processes completed:\n\n"+"\n".join(successes),"Success")


if __name__ == "__main__":
    main()