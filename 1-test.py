import pandas
from common.common import assignval,list_folders,list_folderspaths,makefolder

for folder in list_folders(r"C:\Users\samahalabo\Desktop\5-clips\old"):
    makefolder(r"C:\Users\samahalabo\Desktop\5-clips",folder,start_at_1=False)
