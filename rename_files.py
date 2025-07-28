from common.common import select_folder, windowpath,askstring,custom_dialog,select_anyfile,is_dir
import os
'''
    Args: folder directory or selected files (any type)

    Ouput: fully rename selected to a new word + incremential number (to avoid 2 identical files)
'''

def main():
    from common.common import msgbox
    startpath= windowpath()
    newname = askstring(title='New file name',msg='Enter the new file name')
    if not newname:
        return
    fileorfolder = custom_dialog(msg="Open file or select everything in folder?",op1='file',op2='EVERYTHING')
    if fileorfolder == 'file':
        for file in select_anyfile(title="Select files to rename",path=startpath):
            outputfolder = rename_files(file,newname)
    elif fileorfolder == 'EVERYTHING':
        # outputfolder = select_folder(title="Select FOLDER to rename files inside ",path=startpath)
        if is_dir(startpath):
            for basename in sorted(os.listdir(startpath)): # os.listdir does not provide file names in alphabetical order. Sorted() does so independently of string length
                if os.path.isfile(os.path.join(startpath,basename)):
                    outputfolder = rename_files(os.path.join(startpath,basename),newname)
        else:
            for file in select_anyfile(title="Select files to rename; Invalid startpath",path=startpath):
                outputfolder = rename_files(file,newname)

    os.startfile(outputfolder)
    msgbox(f"Successfully renamed files to: '{newname}'",'Success')

def rename_files(file:str, newname:str,count:int = 1) -> str:
        if os.path.isfile(file):
            
            ext = os.path.splitext(os.path.basename(file))[1]
            newfullpath= os.path.join(os.path.dirname(file),f'{newname}{count}{ext}')
            while os.path.exists(newfullpath):
                count +=1
                newfullpath= os.path.join(os.path.dirname(file),f'{newname}{count}{ext}')
            os.rename(file,newfullpath)
            return os.path.dirname(newfullpath)

if __name__ == "__main__":
    main()