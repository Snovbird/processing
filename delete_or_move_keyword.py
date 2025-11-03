import os,shutil
from common.common import select_folder,windowpath,askstring,list_folderspaths,custom_dialog,list_files,msgbox,list_filespaths

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
    delete_or_move = custom_dialog("Delete or move files to new folder for a certain keyword?","Process","Delete","Move")
    if not delete_or_move:
        return
    folder_path = select_folder(title=f"Select FOLDER to {delete_or_move} files inside",path=startpath)
    if not folder_path:
        return
    stringtodelete = askstring(f"{delete_or_move} files containing the keyword:")
    if not stringtodelete:
        return
    # ifincluded = custom_dialog(msg="Only delete if this string is INCLUDED or EXCLUDED?",title="File name handling",op1='INCLUDED',op2='EXCLUDED')    
    successes = []
    if delete_or_move == "Delete":
        select = custom_dialog("select subfolder or same folder",'Delete in what',"subfolder","same folder")
        if not select:
            return
        if select == "subfolder":
            for folder in list_folderspaths(folder_path):
                count:int = delete_files(folder,stringtodelete)
                successes.append(f"{count} files deleted from {os.path.basename(folder)}")
        elif select == "same folder":
            count:int = delete_files(folder_path,stringtodelete)
            successes.append(f"{count} files deleted from {folder_path}")
        msgbox("Processes completed:\n\n"+"\n".join(successes),"Success")
            
    elif delete_or_move == "Move":
        count = 0
        dst = select_folder("Select dir to move files to")
        for file in list_filespaths(folder_path):
            if stringtodelete in os.path.basename(file):
                shutil.move(file,dst)
                count += 1
        
        msgbox(f"Succesfully moved {count} files to {dst}")

    


if __name__ == "__main__":
    main()