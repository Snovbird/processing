from common.common import select_folder, windowpath,askstring,custom_dialog,select_anyfile,msgbox
import os
'''
    Args: folder directory or selected files (any type)

    Ouput: fully rename selected to a new word + incremential number (to avoid 2 identical files)
'''

def main():
    startpath= windowpath()
    newname = askstring(title='New file name',msg='Enter the new file name')
    if not newname:
        return
    fileorfolder = custom_dialog(msg="Open file or folder dialog?",op1='file',op2='folder')
    if fileorfolder == 'file':
        for file in select_anyfile(title="Select files to rename",path=startpath):
            outputfolder = renamefiles(file,newname)
    elif fileorfolder == 'folder':
        outputfolder = select_folder(title="Select FOLDER to rename files inside ",path=startpath)
        renamefiles(outputfolder,newname)
    else:
        return
    os.startfile(outputfolder)
    msgbox(f"Successfully renamed files to: '{newname}'",'Success')

def renamefiles(file, newname,count=1):
        if os.path.isfile(file):
            
            ext = os.path.splitext(os.path.basename(file))[1]
            newfullpath= os.path.join(os.path.dirname(file),f'{newname}{count}{ext}')
            while os.path.exists(newfullpath):
                count +=1
                newfullpath= os.path.join(os.path.dirname(file),f'{newname}{count}{ext}')
            os.rename(file,newfullpath)
            return os.path.dirname(newfullpath)
        


def renamefilesfolder(folderpath, newname):
    for count, item in enumerate(os.listdir(folderpath)):
        file = os.path.join(folderpath,item)
        if os.path.isfile(file):
            ext = os.path.splitext(item)[1]
            os.rename(file,os.path.join(folderpath,newname + ext))
            print(f'renamed {os.path.join(folderpath,newname + ext)}')


if __name__ == "__main__":
    main()