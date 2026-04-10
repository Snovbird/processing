import os
import shutil
import wx
from common.common import windowpath,select_folder,custom_dialog,askstring,msgbox,error
def main():
    source_folder = windowpath()
    if not os.path.isdir(source_folder):
        source_folder = select_folder("Select folder to rename files or folders inside")
    if not source_folder:
        return
    
    toreplace = askstring("Enter String to REPLACE", 'Str remover')
    append_string = askstring("Enter string to append to filenames:","String Input")
    if append_string:
        START_or_END_or_REPLACE = custom_dialog(msg=f"Place string at the START, END of the file name or simply replace '{toreplace}'",
                                     title='START or END or REPLACE',
                                     op1="REPLACE",op2="START",op3="END",)
    elif not append_string:
        append_string = ''
        START_or_END_or_REPLACE = 'END'
    
    try:
        rename_files(source_folder, append_string,toreplace,START_or_END_or_REPLACE)
        msgbox(f"Successfully renamed targets!", "Success")
    except Exception as e:
        error(str(e))


def rename_files(source_folder, append_string,toreplace,START_or_END_or_REPLACE,file_or_folder=None):
    if not file_or_folder:
        file_or_folder = custom_dialog("Change file or folder names?","Target",op1="File",op2="Folder",op3="Both")
        if not file_or_folder:
            return
    
    if file_or_folder == 'File':
        targets = [f for f in os.listdir(source_folder) 
                if os.path.isfile(os.path.join(source_folder, f))]
    elif file_or_folder == 'Folder':
        targets = [f for f in os.listdir(source_folder) 
                if os.path.isdir(os.path.join(source_folder, f))]
    else: # both
        targets = [f for f in os.listdir(source_folder)]
        
    for target in targets:
        source_file_path = os.path.join(source_folder, target)
        name, extension = os.path.splitext(target)
        if START_or_END_or_REPLACE == 'START':
            new_name = f"{append_string}{name.replace(toreplace,'')}{extension}" # can add a separator if necessary
        elif START_or_END_or_REPLACE == 'END':
            new_name = f"{name.replace(toreplace,'')}{append_string}{extension}" # can add a separator if necessary
        elif START_or_END_or_REPLACE == 'REPLACE':
            new_name = f"{name.replace(toreplace,append_string)}{extension}"   
        os.rename(source_file_path, os.path.join(source_folder,new_name))

if __name__ == "__main__":
    main()
