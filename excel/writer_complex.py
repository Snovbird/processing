import pandas,os
from .general import fit_columns


def writer_complex(data:dict[str , dict[str,list[str|int]]],xlsx_path:str="output.xlsx"):
    """
    Args:
    data: {"Sheet Name": {"Column Name": [ data, data] } }.
    xlsx_path: Full or relative path ending by `.xlsx`
    You can also alternate "str" title and int data to have data in same column
    """
    with pandas.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
        
        for sheet_name, columns_data in data.items():

            columns_data:dict[str, list[str|int]]

            dataframe = pandas.DataFrame(columns_data)

            dataframe.to_excel(writer, sheet_name=sheet_name, index=False,header=True)

            fit_columns(writer.sheets[sheet_name])
    
    return xlsx_path

if __name__ == "__main__":

    test_data = {f"Sheet {i}": {f"column {i}":[i for i in range(10)] for i in range(6)} for i in range (3)}

    os.startfile(
        writer_complex(test_data)
        )