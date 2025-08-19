import pandas,wx
from .simplecommon import error,select_folder

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

def excel_to_dict(file_path: str) -> dict[str, list[int | str]]:
    """

    Args:
    file_path: Path to Excel .xlsx file

    Returns:
    Dictionary where keys are column headers and values are lists of column values
    """
    import ast
    try:
        df = pandas.read_excel(file_path, sheet_name=0)
        return {col: [ast.literal_eval(item) if isinstance(item, str) else item 
                     for item in df[col].tolist()] for col in df.columns}
    except Exception as e:
        error(f"Cannot read '{file_path}'. Conversion to dict failed: {e}")
        return None