import os
import pandas as pd
import ast
from tkinter import Tk, filedialog

def analyze_excel_files():
    # Initialize dictionary to store counts
    occurrence_dict = {}
    
    # Ask for folder directory using a dialog
    root = Tk()
    root.withdraw()  # Hide the main window
    directory = filedialog.askdirectory(title="Select the parent directory")
    root.destroy()
    
    if not directory:
        print("No directory selected. Exiting program.")
        return
    
    # Get all subfolders in the directory
    subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
    
    if not subfolders:
        print(f"No subfolders found in {directory}")
        return
    
    print(f"Found {len(subfolders)} subfolders to process.")
    
    # Process each subfolder
    for subfolder in subfolders:
        excel_path = os.path.join(subfolder, "ACTIVE_all_event_probability.xlsx")
        
        if os.path.exists(excel_path):
            try:
                # Read the Excel file
                df = pd.read_excel(excel_path)
                
                # Process column 2 (index 1) starting from row 2 (index 1)
                for i in range(1, len(df)):
                    cell_value = df.iloc[i, 1]  # Get value from column 2 (index 1)
                    
                    if pd.notna(cell_value):  # Check if cell is not empty
                        try:
                            # Convert string list to actual list and get first element
                            key = ast.literal_eval(str(cell_value))[0]
                            
                            # Update dictionary
                            if key in occurrence_dict:
                                occurrence_dict[key] += 1
                            else:
                                occurrence_dict[key] = 1
                                
                        except (SyntaxError, ValueError) as e:
                            print(f"Error processing value '{cell_value}' in {excel_path}: {e}")
                
                print(f"Processed {excel_path}")
                
            except Exception as e:
                print(f"Error processing file {excel_path}: {e}")
        else:
            print(f"Excel file not found in {subfolder}")
    
    # Print results
    if occurrence_dict:
        print("\nResults:")
        print("-" * 40)
        for key, count in sorted(occurrence_dict.items()):
            print(f"{key}: {count}")
    else:
        print("No data was processed.")

if __name__ == "__main__":
    analyze_excel_files()
