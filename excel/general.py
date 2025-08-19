import pandas,wx
from .common import error,select_folder

def fit_columns(worksheet):
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

def excel_to_list(file_path:str) -> list[list[int | str]]:
    """
    Returns:
    
    """
    import ast
    try:
        df = pandas.read_excel(file_path, sheet_name=0)
        return [[ast.literal_eval(item) if isinstance(item, str) else item # index 0 = behavior name. Index 1 = probability
                for item in df[col].tolist()] for col in df.columns]
    except Exception as e:
        error(f"Cannot read '{file_path}'. Conversion to list failed: {e}")
        return None
