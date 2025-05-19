import os
import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

def rename_files_from_subfolders():
    # Create the main window
    root = tk.Tk()
    root.title("Subfolder File Renamer")
    root.geometry("600x400")
    
    # Variable to store selected folder path
    selected_folder = filedialog.askdirectory(
        title="Select parent folder",
    )
    folder_dir_with_files_to_delete = filedialog.askdirectory(
        title="Select parent folder",
    )
    
    # Function to process files in subfolders
    def process_files(folder_path):
        
        if not folder_path:
            messagebox.showwarning("Warning", "Please select a parent folder first!")
            return
        
        try:    
            # Determine where to create the "rename" folder - at the same level as the selected folder
            parent_dir = os.path.dirname(folder_path)
            rename_folder = os.path.join(parent_dir, "rename")
            
            # Create the rename folder if it doesn't exist
            if not os.path.exists(rename_folder):
                os.makedirs(rename_folder)
            
            total_renamed = 0
            
            # Get all subfolders from the selected folder
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            
            # Process each subfolder
            for subfolder in subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                
                # Find files with "2a_trimmed" in their names
                renamed_in_subfolder = 0
                for root_dir, dirs, files in os.walk(subfolder_path):
                    for file in files:
                        # Check if file contains "2a_trimmed"
                        if "-marked-trim" in file:
                            file_path = os.path.join(root_dir, file)
                            
                            # Create the new filename by replacing "2a_trimmed" with subfolder name
                            new_filename = subfolder + "_" + file.replace("-marked-trim", "")
                            new_path = os.path.join(rename_folder, new_filename)
                            
                            # Handle duplicate filenames
                            counter = 1
                            base_name, ext = os.path.splitext(new_filename)
                            while os.path.exists(new_path):
                                new_filename = f"{base_name}_{counter}{ext}"
                                new_path = os.path.join(rename_folder, new_filename)
                                counter += 1
                            
                            # Copy the file to the rename folder with new name
                            shutil.copy2(file_path, new_path)
                            root.update()
                            renamed_in_subfolder += 1
                            total_renamed += 1
                
                root.update()
            
            # Show completion message
            if total_renamed > 0:
                messagebox.showinfo("Success", f"Successfully renamed and copied {total_renamed} files to {rename_folder}")
                # Open the folder in explorer/finder
                if os.name == 'nt':  # Windows
                    os.startfile(rename_folder)
            else:
                messagebox.showinfo("Information", "No files with '2a_trimmed' were found in any subfolder")
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            messagebox.showerror("Error", error_msg)
    root.destroy()
    process_files(selected_folder)

if __name__ == "__main__":
    rename_files_from_subfolders()