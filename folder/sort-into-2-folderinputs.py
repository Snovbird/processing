import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import shutil

def sort_files_by_keywords():
    # Create the main window but keep it hidden
    root = tk.Tk()
    root.withdraw()
    
    # Get the first input: folder containing files to sort
    source_folder = filedialog.askdirectory(title="Select folder containing files to sort")
    if not source_folder:
        messagebox.showwarning("Warning", "No folder selected!")
        return
    
    # Get the second input: string containing keywords (set 1)
    keywords_set1 = simpledialog.askstring("Input", "Enter first set of keywords separated by periods (e.g. key1.key2.key3)")
    if not keywords_set1:
        messagebox.showwarning("Warning", "No keywords provided for first set!")
        return
    
    # Get the third input: string associated with keywords set 1
    folder_name_set1 = simpledialog.askstring("Input", "Enter folder name for files matching first set of keywords")
    if not folder_name_set1:
        messagebox.showwarning("Warning", "No folder name provided for first set!")
        return
    
    # Get the fourth input: string containing keywords (set 2)
    keywords_set2 = simpledialog.askstring("Input", "Enter second set of keywords separated by periods (e.g. key1.key2.key3)")
    if not keywords_set2:
        messagebox.showwarning("Warning", "No keywords provided for second set!")
        return
    
    # Get the fifth input: string associated with keywords set 2
    folder_name_set2 = simpledialog.askstring("Input", "Enter folder name for files matching second set of keywords")
    if not folder_name_set2:
        messagebox.showwarning("Warning", "No folder name provided for second set!")
        return
    
    # Convert keyword strings to lists
    keywords_list1 = [k.strip() for k in keywords_set1.split('.')]
    keywords_list2 = [k.strip() for k in keywords_set2.split('.')]
    
    # Create destination folders
    parent_dir = os.path.dirname(source_folder)
    dest_folder1 = os.path.join(parent_dir, folder_name_set1)
    dest_folder2 = os.path.join(parent_dir, folder_name_set2)
    
    # Ensure dest_folder2 has a unique name if folder_name_set1 == folder_name_set2
    if folder_name_set1 == folder_name_set2:
        folder_name_set2 = f"{folder_name_set2}_2"
        dest_folder2 = os.path.join(parent_dir, folder_name_set2)
    
    if not os.path.exists(dest_folder1):
        os.makedirs(dest_folder1)
    
    if not os.path.exists(dest_folder2):
        os.makedirs(dest_folder2)
    
    # Track statistics
    count_set1 = 0
    count_set2 = 0
    
    try:
        # Scan files in source directory
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Check if file contains any keyword from set 1
            if any(keyword in filename for keyword in keywords_list1):
                shutil.copy2(file_path, os.path.join(dest_folder1, filename))
                count_set1 += 1
            
            # Check if file contains any keyword from set 2
            if any(keyword in filename for keyword in keywords_list2):
                shutil.copy2(file_path, os.path.join(dest_folder2, filename))
                count_set2 += 1
        
        # Show completion message
        messagebox.showinfo("Success", f"Files sorted successfully!\n\n{count_set1} files copied to '{folder_name_set1}'\n{count_set2} files copied to '{folder_name_set2}'")
        
        # Open the parent directory
        if os.name == 'nt':  # Windows
            os.startfile(parent_dir)
        elif os.name == 'posix':  # macOS or Linux
            import subprocess
            if 'darwin' in os.uname()[0].lower():  # macOS
                subprocess.call(['open', parent_dir])
            else:  # Linux
                subprocess.call(['xdg-open', parent_dir])
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    root.destroy()

if __name__ == "__main__":
    sort_files_by_keywords()
