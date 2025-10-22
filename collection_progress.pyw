import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation

def update_folders_excel(folder_dir, excel_file_path):
    """
    Updates an Excel file with folder names from a directory.
    Adds missing folders to column 1 and creates checkboxes in column 2.
    
    Args:
        folder_dir (str): Path to the directory containing folders
        excel_file_path (str): Path to the Excel file to update
    """
    
    # Get list of folders in the input directory
    try:
        all_items = os.listdir(folder_dir)
        folder_names = [item for item in all_items 
                       if os.path.isdir(os.path.join(folder_dir, item))]
        print(f"Found {len(folder_names)} folders in directory: {folder_names}")
    except FileNotFoundError:
        print(f"Error: Directory '{folder_dir}' not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied accessing '{folder_dir}'.")
        return
    
    # Read existing Excel file or create new DataFrame
    try:
        if os.path.exists(excel_file_path):
            df = pd.read_excel(excel_file_path)
            print(f"Loaded existing Excel file with {len(df)} rows")
        else:
            df = pd.DataFrame(columns=['Folder Name', 'Checkbox'])
            print("Created new DataFrame as Excel file doesn't exist")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return
    
    # Ensure proper column names
    if df.empty:
        df = pd.DataFrame(columns=['Folder Name', 'Checkbox'])
    else:
        # Rename first two columns if they exist
        columns = df.columns.tolist()
        if len(columns) >= 1:
            df.rename(columns={columns[0]: 'Folder Name'}, inplace=True)
        if len(columns) >= 2:
            df.rename(columns={columns[1]: 'Checkbox'}, inplace=True)
        elif len(columns) == 1:
            df['Checkbox'] = ''
    
    # Get existing folder names in Excel (case-insensitive comparison)
    existing_folders = set()
    if 'Folder Name' in df.columns and not df['Folder Name'].isna().all():
        existing_folders = set(df['Folder Name'].dropna().astype(str).str.lower())
    
    # Find folders that need to be added
    folders_to_add = []
    for folder in folder_names:
        if folder.lower() not in existing_folders:
            folders_to_add.append(folder)
    
    print(f"Folders to add: {folders_to_add}")
    
    # Add missing folders to DataFrame
    if folders_to_add:
        new_rows = pd.DataFrame({
            'Folder Name': folders_to_add,
            'Checkbox': ['☐'] * len(folders_to_add)  # Empty checkbox symbol
        })
        df = pd.concat([df, new_rows], ignore_index=True)
        print(f"Added {len(folders_to_add)} new folders")
    else:
        print("No new folders to add")
    
    # Save updated DataFrame to Excel
    try:
        df.to_excel(excel_file_path, index=False, engine='openpyxl')
        print(f"Successfully updated Excel file: {excel_file_path}")
        
        # Add data validation for checkboxes using openpyxl
        
    except Exception as e:
        print(f"Error saving Excel file: {e}")


# Example usage
if __name__ == "__main__":
    # Get user inputs
    folder_directory = r"C:\Users\samahalabo\Desktop\0-RECORDINGS"
    excel_file = r"C:\Users\samahalabo\Desktop\Collection progress.xlsx"
    
    # Validate inputs
    if not folder_directory or not excel_file:
        print("Please provide both folder directory and Excel file paths.")
    else:
        # Ensure Excel file has .xlsx extension
        if not excel_file.endswith(('.xlsx', '.xls')):
            excel_file += '.xlsx'
        
        # Run the update function
        update_folders_excel(folder_directory, excel_file)
