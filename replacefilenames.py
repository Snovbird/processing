from common.common import select_folder, windowpath,askstring,custom_dialog,select_anyfile,msgbox
import os
'''
    Args: folder directory or selected files (any type)

    Ouput: fully rename selected to a new word + incremential number (to avoid 2 identical files)
'''

def main():
    startpath= windowpath()

    fileorfolder = custom_dialog(msg="Open file or folder dialog?",op1='file',op2='folder')
    newname = askstring(title='New file name',question='Enter the new file name')
    if fileorfolder == 'file':
        for file in select_anyfile(title="Select files to rename",path=startpath):
            renamefiles(file)
    elif fileorfolder == 'folder':
        folderpath = select_folder(title="Select FOLDER to rename files inside ",path=startpath)
        renamefiles(folderpath,newname)
    else:
        return

    os.startfile(folderpath)
    msgbox(f"Successfully renamed files to: '{newname}'",'Success')

def renamefiles(file, newname,count=0):
        if os.path.isfile(file):
            
            ext = os.path.splitext(os.path.basename(file))[1]
            newfullpath= os.path.join(os.path.dirname(file),newname + count + ext)
            while os.path.exists(newfullpath):
                count +=1
            os.rename(file,newfullpath)


def renamefilesfolder(folderpath, newname):
    for count, item in enumerate(os.listdir(folderpath)):
        file = os.path.join(folderpath,item)
        if os.path.isfile(file):
            ext = os.path.splitext(item)[1]
            os.rename(file,os.path.join(folderpath,newname + ext))


if __name__ == "__main__":
    main()