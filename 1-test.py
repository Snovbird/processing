import pandas,os
from common.common import assignval,list_folders,list_folderspaths,makefolder,simple_file_walk,msgbox

def thefunc(file):
    dir = os.path.dirname(file)
    newname = os.path.basename(file).replace("Annotated video","Annotated video.avi").replace("2-FN-light","FNCL").replace('3-FF-light','FFCL').replace('4-BF-light','BFCL').replace('5-BN-light','BNCL')
    os.rename(file,os.path.join(dir,newname))

msgbox(f"{simple_file_walk(r"C:\Users\samahalabo\Desktop\9-ANALYSIS\detector test",thefunc)} files renamed")