import pandas
import os
from common.common import error,msgbox,select_anyfile
import pandas as pd

def excel_columns_to_lists(file_path):
    """
    Read the first tab of an Excel file and assign all columns to separate lists
    
    Args:
        file_path (str): Path to the Excel file
    
    Returns:
        dict: Dictionary where keys are column names and values are lists of column data
    """
    try:
        # Read the first sheet of the Excel file
        df = pd.read_excel(file_path, sheet_name=0)  # sheet_name=0 gets the first tab
        
        # Check if DataFrame is empty
        if df.empty:
            print("Warning: The Excel file is empty!")
            return {}
        
        # Convert each column to a list and store in dictionary
        column_lists = {}
        for column in df.columns:
            column_lists[column] = df[column].tolist()
            print(f"Column '{column}': {len(column_lists[column])} items")
        
        print(f"\nSuccessfully extracted {len(column_lists)} columns from '{file_path}'")
        return column_lists
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
        return {}
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return {}

# Even simpler one-liner version
def simple_excel_to_lists(file_path):
    """One-liner version"""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        return {col: df[col].tolist() for col in df.columns}
    except: # df.empty
        return {}

def count_continuous_sets(lst, min_length=4, max_gap=3):
    """Ultra-optimized version with numpy key conversion"""
    if not lst:
        return {}
    
    try:
        import numpy as np
        arr = np.array(lst)
        
        # Find change points
        changes = np.where(arr[:-1] != arr[1:])[0] + 1
        starts = np.concatenate(([0], changes))
        ends = np.concatenate((changes, [len(arr)]))
        
        # Group by value
        result = {}
        for value in np.unique(arr):
            mask = arr[starts] == value
            value_starts = starts[mask]
            value_lengths = (ends - starts)[mask]
            
            # Merge close groups and count
            if len(value_starts) == 1:
                result[value] = 1 if value_lengths[0] >= min_length else 0
            else:
                gaps = value_starts[1:] - (value_starts[:-1] + value_lengths[:-1])
                merge_points = gaps > max_gap
                
                qualifying_count = 0
                current_total = value_lengths[0]
                
                for i, should_split in enumerate(merge_points):
                    if should_split:
                        if current_total >= min_length:
                            qualifying_count += 1
                        current_total = value_lengths[i + 1]
                    else:
                        current_total += value_lengths[i + 1]
                
                if current_total >= min_length:
                    qualifying_count += 1
                    
                result[value] = qualifying_count
        
        # Convert numpy keys to Python integers
        final_result = {}
        for key, value in result.items():
            final_result[int(key.item() if hasattr(key, 'item') else key)] = value
        
        return final_result
    except:
        pass
    # except ImportError:
    #     return count_continuous_sets(lst, min_length, max_gap)    

import pandas as pd
from common.common import select_folder, makefolder
import os

def dict_to_excel(data_dict, output_path=None, filename="output.xlsx"):
    """
    Create an Excel file with dictionary keys in row 1 and values in row 2.
    
    Args:
        data_dict (dict): Dictionary to convert to Excel
        output_path (str): Directory path to save the file (optional)
        filename (str): Name of the Excel file (default: "output.xlsx")
    
    Returns:
        str: Full path to the created Excel file
    """
    try:
        # If no output path provided, ask user to select folder
        if not output_path:
            output_path = select_folder("Select folder to save Excel file")
            if not output_path:
                return None
        
        # Ensure filename has .xlsx extension
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        # Create full file path
        full_path = os.path.join(output_path, filename)
        
        # Create DataFrame with keys as column headers and values as first row
        df = pd.DataFrame([data_dict])
        
        # Write to Excel
        df.to_excel(full_path, index=False, header=True)
        
        print(f"Excel file created successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return None

# Alternative version with more control over formatting
def dict_to_excel_advanced(data_dict, output_path=None, filename="ACTUAL behavior counts.xlsx", sheet_name="behavior counts"):
    """
    Advanced version with more formatting options.
    """
    try:
        if not output_path:
            output_path = select_folder("Select folder to save Excel file")
            if not output_path:
                return None
        
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        full_path = os.path.join(output_path, filename)
        
        # Create Excel writer object for more control
        with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
            # Create DataFrame
            df = pd.DataFrame([data_dict])
            
            # Write to Excel
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=True)
            
            # Optional: Access workbook for additional formatting
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Excel file created successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error creating Excel file: {str(e)}")
        return None

# Integration with your existing code
def main():
    excel_path = select_anyfile("Find the excel file containing data", specific_ext="xlsx")[0]
    if not excel_path:
        return
    col1, col2, *_ = excel_columns_to_lists(excel_path).values()

    new_counts = count_continuous_sets(col2)
    
    # Create Excel file from the results
    output_file = dict_to_excel(
        new_counts, 
        output_path=os.path.dirname(excel_path),  # Save in same folder as input
        filename="behavior_counts_results.xlsx"
    )
    
    if output_file:
        print(f"Results saved to: {output_file}")
        # Optional: Open the file
        os.startfile(output_file)

def main():
    excel_path = select_anyfile("Find the excel file containing data",specific_ext="xlsx")[0]
    if not excel_path:
        return
    col1, col2, *_ = excel_columns_to_lists(excel_path).values()

    new_counts = count_continuous_sets(col2) # I want ordered sets, not a dictionnary
    
    dict_to_excel_advanced(new_counts, output_path=os.path.dirname(excel_path),)
# Usage examples:
if __name__ == "__main__":
    # Method 1: Detailed function with error handling
    main()