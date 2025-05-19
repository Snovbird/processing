import os
import tkinter as tk
from tkinter import filedialog, messagebox

def delete_matching_files():
    # Create the main window
    root = tk.Tk()
    root.title("File Matcher and Deleter")
    root.withdraw()  # Hide the main window since we're just using dialogs
    
    # Ask for folder containing reference files
    selected_folder = filedialog.askdirectory(
        title="Select folder containing reference files",
    )
    
    if not selected_folder:
        messagebox.showwarning("Warning", "No reference folder selected!")
        return
    
    # Ask for folder containing files that might be deleted
    folder_dir_with_files_to_delete = filedialog.askdirectory(
        title="Select folder containing files to potentially delete",
    )
    
    if not folder_dir_with_files_to_delete:
        messagebox.showwarning("Warning", "No target folder selected!")
        return
    
    try:
        # Get all files in the folder_dir_with_files_to_delete
        files_to_check = [f for f in os.listdir(folder_dir_with_files_to_delete) 
                         if os.path.isfile(os.path.join(folder_dir_with_files_to_delete, f))]
        
        deleted_count = 0
        
        # Walk through all files in selected_folder and check for matches
        for root_dir, _, files in os.walk(selected_folder):
            for file in files:
                if file in files_to_check:
                    file_path = os.path.join(folder_dir_with_files_to_delete, file)
                    os.remove(file_path)
                    deleted_count += 1
        
        # Show completion message
        if deleted_count > 0:
            messagebox.showinfo("Success", f"Successfully deleted {deleted_count} matching files from {folder_dir_with_files_to_delete}")
        else:
            messagebox.showinfo("Information", "No matching files were found to delete")
            
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        messagebox.showerror("Error", error_msg)

if __name__ == "__main__":
    delete_matching_files()
