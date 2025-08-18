import pandas, os
from excel.general import fit_columns

path = "pandas_tutorial_output.xlsx" # This file will be created in the same directory as the script

with pandas.ExcelWriter(path, engine='openpyxl') as writer:

    sheet_name :str = "sheet one" 

    # automatically considers keys as column headers
    column_data:dict[str, list[int]] = {"happy": [1, 2, 3], "unhappy": [4, 5, 6]}

    dataframe = pandas.DataFrame(column_data)

    # writer.sheets is a dictionnary: {'sheet one': <Worksheet "sheet one">}
    dataframe.to_excel(writer, sheet_name=f"{sheet_name}",index=False,header=True)
    # writer.sheets[sheet_name] gives you the openpyxl Worksheet object for the sheet

    # adjust columns to width
    fit_columns(writer.sheets[sheet_name])


os.startfile('pandas_tutorial_output.xlsx')
