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

# Example usage
def example_usage():
    """Example of how to use the function"""
    
    # Replace with your Excel file path
    file_path = "your_file.xlsx"
    
    # Get all columns as lists
    columns = excel_columns_to_lists(file_path) # {column name : column data}
    
    # Access individual column lists
    if columns:
        for column_name, column_data in columns.items():
            print(f"\n{column_name}:")
            print(f"First 5 values: {column_data[:5]}")
            print(f"Data type: {type(column_data[0]) if column_data else 'Empty'}")

# Even simpler one-liner version
def simple_excel_to_lists(file_path):
    """One-liner version"""
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        return {col: df[col].tolist() for col in df.columns}
    except: # df.empty
        return {}

def count_continuous_sets(lst, min_length=4, max_gap=3):
    """
    Count continuous sets of values that meet the minimum length requirement.
    Sets separated by max_gap or fewer different values are considered the same set.
    
    Args:
        lst: Input list of values
        min_length: Minimum length for a set to be counted (default 4)
        max_gap: Maximum gap between sets to consider them as one (default 3)
    
    Returns:
        Dictionary with counts of qualifying sets for each value
    """
    if not lst:
        return {}
    
    # Group consecutive identical values with their positions
    groups = []
    current_value = lst[0]
    current_start = 0
    current_count = 1
    
    for i in range(1, len(lst)):
        if lst[i] == current_value:
            current_count += 1
        else:
            groups.append((current_value, current_start, current_count))
            current_value = lst[i]
            current_start = i
            current_count = 1
    
    # Add the last group
    groups.append((current_value, current_start, current_count))
    
    # Merge groups of same value that are separated by max_gap or less
    merged_sets = {}
    
    for value, start, count in groups:
        if value not in merged_sets:
            merged_sets[value] = []
        merged_sets[value].append((start, count))
    
    # For each value, merge close groups and count qualifying sets
    result = {}
    
    for value, positions in merged_sets.items():
        merged_groups = []
        current_total = positions[0][1]  # count of first group
        current_end = positions[0][0] + positions[0][1]  # end position of first group
        
        for i in range(1, len(positions)):
            start_pos, count = positions[i]
            gap = start_pos - current_end
            
            if gap <= max_gap:
                # Merge with current group
                current_total += count
                current_end = start_pos + count
            else:
                # Start new group
                if current_total >= min_length:
                    merged_groups.append(current_total)
                current_total = count
                current_end = start_pos + count
        
        # Don't forget the last group
        if current_total >= min_length:
            merged_groups.append(current_total)
        
        result[value] = len(merged_groups)
    
    # Ensure all unique values from the list are in the result
    for value in set(lst):
        if value not in result:
            result[value] = 0
    
    return result

# Test with your example
test_list = [1,1,1,1,2,2,1,1,1,1,3,3,3,1,1,3,3,3,3,2,2,2,4,4,4,4]
print(count_continuous_sets(test_list))
# Output: {1: 1, 2: 0, 3: 1, 4: 1}

# You can adjust the parameters:
# count_continuous_sets(test_list, min_length=5, max_gap=2)


def main():
    excel_path = select_anyfile("Find the data excel",specific_ext="xlsx")
    if not excel_path:
        return
    columns = simple_excel_to_lists(excel_path)
    
    missing_counts = 
    
# Usage examples:
if __name__ == "__main__":
    # Method 1: Detailed function with error handling
    columns = excel_columns_to_lists("data.xlsx")
    
    # Method 2: Simple one-liner
    columns_simple = simple_excel_to_lists("data.xlsx")
    
    # Access specific columns
    if 'Sales' in columns:
        sales_list = columns['Sales']
        print(f"Sales data: {sales_list}")