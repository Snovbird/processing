import pandas,os
from .common import select_folder
def export_excel(data_dict: dict[str, list[dict[str, str | int]]], output_path=None, filename="CORRECTED behavior data.xlsx"):
    """
    Create Excel file with separate sheets for each video.
    Each behavior becomes a column, with behavior names as column headers.
    """
    try:
        if not output_path:
            output_path = select_folder("Select folder to save Excel file")
            if not output_path:
                return None
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        full_path = os.path.join(output_path, filename)
        
        with pandas.ExcelWriter(full_path, engine='openpyxl') as writer:
            
            for video_name, behavior_list in data_dict.items():
                if not behavior_list:
                    continue
                
                # Create a DataFrame where each row represents one behavior instance
                df = pandas.DataFrame(behavior_list)
                
                # Clean sheet name
                clean_sheet_name = str(video_name).replace('/', '_').replace('\\', '_')[:31]
                
                # Write to Excel
                df.to_excel(writer, sheet_name=clean_sheet_name, index=False, header=True) 
                
                # Format the sheet
                workbook = writer.book
                worksheet = writer.sheets[clean_sheet_name]
                
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
        
        print(f"Excel file created successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return None
