from excel.general import excel_to_list, list_to_excel
from common.common import *

tolist = select_folder()
outpath = r"C:\Users\samahalabo\Desktop\4-detector\2.Trained detector"

list_to_excel(list_folders(tolist), default_file_name="folders1.xlsx")