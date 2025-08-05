import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample datasets for demonstration"""
    
    # Sample sales data
    sales_data = {
        'Date': pd.date_range('2024-01-01', periods=100, freq='D'),
        'Product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor'], 100),
        'Sales_Amount': np.random.randint(100, 2000, 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    }
    
    # Sample employee data
    employee_data = {
        'Employee_ID': range(1, 51),
        'Name': [f'Employee_{i}' for i in range(1, 51)],
        'Department': np.random.choice(['IT', 'Sales', 'Marketing', 'HR'], 50),
        'Salary': np.random.randint(40000, 120000, 50),
        'Years_Experience': np.random.randint(1, 15, 50)
    }
    
    # Sample inventory data (intentionally empty for error handling demo)
    inventory_data = {
        'Product_ID': [],
        'Product_Name': [],
        'Stock_Level': [],
        'Reorder_Point': []
    }
    
    return (pd.DataFrame(sales_data), 
            pd.DataFrame(employee_data), 
            pd.DataFrame(inventory_data))

def assign_columns_rows_to_lists(df, df_name):
    """
    Assign different columns and rows to separate lists
    """
    print(f"\n--- Processing {df_name} DataFrame ---")
    
    if df.empty:
        print(f"Warning: {df_name} DataFrame is empty!")
        return {}, {}
    
    # Assign columns to separate lists
    column_lists = {}
    for column in df.columns:
        column_lists[column] = df[column].tolist()
        print(f"{column} list length: {len(column_lists[column])}")
    
    # Assign specific rows to separate lists
    row_lists = {}
    
    # First 5 rows
    if len(df) >= 5:
        row_lists['first_5_rows'] = df.head(5).values.tolist()
        print(f"First 5 rows extracted: {len(row_lists['first_5_rows'])} rows")
    
    # Last 5 rows
    if len(df) >= 5:
        row_lists['last_5_rows'] = df.tail(5).values.tolist()
        print(f"Last 5 rows extracted: {len(row_lists['last_5_rows'])} rows")
    
    # Random 10 rows (if available)
    if len(df) >= 10:
        random_indices = np.random.choice(df.index, size=min(10, len(df)), replace=False)
        row_lists['random_10_rows'] = df.loc[random_indices].values.tolist()
        print(f"Random 10 rows extracted: {len(row_lists['random_10_rows'])} rows")
    
    return column_lists, row_lists

def write_to_excel_with_error_handling(dataframes_dict, filename='pandas_tutorial_output.xlsx'):
    """
    Write multiple DataFrames to different Excel tabs with comprehensive error handling
    """
    
    try:
        # Check if any dataframes exist
        if not dataframes_dict:
            raise ValueError("No dataframes provided to write to Excel")
        
        # Create Excel writer object
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            tabs_created = 0
            
            for sheet_name, df in dataframes_dict.items():
                try:
                    # Check if DataFrame is empty
                    if df.empty:
                        print(f"Warning: {sheet_name} is empty. Creating tab with 'No Data' message.")
                        
                        # Create a DataFrame with a "No Data" message
                        no_data_df = pd.DataFrame({
                            'Message': ['No data available for this sheet'],
                            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                            'Sheet_Name': [sheet_name]
                        })
                        
                        no_data_df.to_excel(writer, sheet_name=sheet_name, index=False)
                        
                    else:
                        # Write the actual data
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"Successfully wrote {len(df)} rows to '{sheet_name}' tab")
                    
                    tabs_created += 1
                    
                except Exception as sheet_error:
                    print(f"Error writing sheet '{sheet_name}': {str(sheet_error)}")
                    
                    # Create error sheet
                    error_df = pd.DataFrame({
                        'Error': [f"Failed to write {sheet_name}"],
                        'Error_Message': [str(sheet_error)],
                        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
                    })
                    
                    try:
                        error_df.to_excel(writer, sheet_name=f"{sheet_name}_ERROR", index=False)
                        tabs_created += 1
                    except:
                        print(f"Could not create error sheet for {sheet_name}")
        
        print(f"\nExcel file '{filename}' created successfully with {tabs_created} tabs!")
        return True
        
    except Exception as e:
        print(f"Critical error creating Excel file: {str(e)}")
        return False

def analyze_data_and_create_summaries(sales_df, employee_df):
    """
    Create summary DataFrames for additional Excel tabs
    """
    summaries = {}
    
    try:
        if not sales_df.empty:
            # Sales summary by product
            sales_summary = sales_df.groupby('Product').agg({
                'Sales_Amount': ['sum', 'mean', 'count'],
                'Quantity': 'sum'
            }).round(2)
            
            # Flatten column names
            sales_summary.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count', 'Total_Quantity']
            sales_summary = sales_summary.reset_index()
            summaries['Sales_Summary'] = sales_summary
            
            # Regional analysis
            regional_summary = sales_df.groupby('Region')['Sales_Amount'].agg(['sum', 'mean', 'count']).round(2)
            regional_summary.columns = ['Total_Sales', 'Avg_Sales', 'Transaction_Count']
            regional_summary = regional_summary.reset_index()
            summaries['Regional_Analysis'] = regional_summary
            
    except Exception as e:
        print(f"Error creating sales summaries: {str(e)}")
    
    try:
        if not employee_df.empty:
            # Department summary
            dept_summary = employee_df.groupby('Department').agg({
                'Salary': ['mean', 'min', 'max', 'count'],
                'Years_Experience': 'mean'
            }).round(2)
            
            # Flatten column names
            dept_summary.columns = ['Avg_Salary', 'Min_Salary', 'Max_Salary', 'Employee_Count', 'Avg_Experience']
            dept_summary = dept_summary.reset_index()
            summaries['Department_Summary'] = dept_summary
            
    except Exception as e:
        print(f"Error creating employee summaries: {str(e)}")
    
    return summaries

def main():
    """
    Main tutorial function demonstrating pandas operations
    """
    
    print("=== Pandas Tutorial: Columns/Rows to Lists & Excel Export ===\n")
    
    # Step 1: Create sample data
    print("Step 1: Creating sample datasets...")
    sales_df, employee_df, inventory_df = create_sample_data()
    
    # Step 2: Assign columns and rows to separate lists
    print("\nStep 2: Assigning columns and rows to separate lists...")
    
    # Process each DataFrame
    sales_columns, sales_rows = assign_columns_rows_to_lists(sales_df, "Sales")
    employee_columns, employee_rows = assign_columns_rows_to_lists(employee_df, "Employee")
    inventory_columns, inventory_rows = assign_columns_rows_to_lists(inventory_df, "Inventory")
    
    # Step 3: Demonstrate list operations
    print("\nStep 3: Demonstrating list operations...")
    
    if sales_columns:
        print(f"Sales Amount range: ${min(sales_columns['Sales_Amount'])} - ${max(sales_columns['Sales_Amount'])}")
        print(f"Unique products: {set(sales_columns['Product'])}")
    
    if employee_columns:
        print(f"Salary range: ${min(employee_columns['Salary'])} - ${max(employee_columns['Salary'])}")
        print(f"Departments: {set(employee_columns['Department'])}")
    
    # Step 4: Create summary analyses
    print("\nStep 4: Creating summary analyses...")
    summaries = analyze_data_and_create_summaries(sales_df, employee_df)
    
    # Step 5: Prepare data for Excel export
    print("\nStep 5: Preparing data for Excel export...")
    
    excel_data = {
        'Raw_Sales_Data': sales_df,
        'Raw_Employee_Data': employee_df,
        'Raw_Inventory_Data': inventory_df,  # This will be empty - demonstrates error handling
    }
    
    # Add summaries
    excel_data.update(summaries)
    
    # Step 6: Write to Excel with error handling
    print("\nStep 6: Writing to Excel with error handling...")
    success = write_to_excel_with_error_handling(excel_data)
    
    if success:
        print("\n=== Tutorial completed successfully! ===")
        print("Check the 'pandas_tutorial_output.xlsx' file to see the results.")
        print("\nKey features demonstrated:")
        print("✓ Column data assigned to separate lists")
        print("✓ Row data assigned to separate lists")
        print("✓ Multiple Excel tabs created")
        print("✓ Error handling for empty DataFrames")
        print("✓ Summary statistics and analysis")
    else:
        print("\n=== Tutorial completed with errors ===")
        print("Please check the error messages above.")

# Additional utility functions for advanced operations
def demonstrate_advanced_list_operations(df):
    """
    Advanced operations with column/row lists
    """
    if df.empty:
        return
    
    print(f"\n--- Advanced List Operations ---")
    
    # Convert specific columns to different data types in lists
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    print(f"Numeric columns: {numeric_columns}")
    print(f"Categorical columns: {categorical_columns}")
    
    # Create filtered lists based on conditions
    if 'Sales_Amount' in df.columns:
        high_sales = df[df['Sales_Amount'] > df['Sales_Amount'].median()]['Sales_Amount'].tolist()
        print(f"High sales values (above median): {len(high_sales)} items")
    
    # Create nested lists (rows as lists of lists)
    rows_as_lists = [row.tolist() for _, row in df.iterrows()]
    print(f"Total rows converted to nested lists: {len(rows_as_lists)}")

if __name__ == "__main__":
    main()
    
    # Bonus: Demonstrate advanced operations
    print("\n" + "="*50)
    print("BONUS: Advanced List Operations")
    print("="*50)
    
    sales_df, _, _ = create_sample_data()
    demonstrate_advanced_list_operations(sales_df)

