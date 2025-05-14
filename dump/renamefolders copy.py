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
    selected_folder = tk.StringVar()
    
    # Frame for displaying the selected folder
    folder_frame = tk.Frame(root)
    folder_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)
    
    tk.Label(folder_frame, text="Selected Parent Folder:").pack(anchor=tk.W)
    folder_path_label = tk.Label(folder_frame, textvariable=selected_folder, relief=tk.SUNKEN, anchor=tk.W, width=70)
    folder_path_label.pack(fill=tk.X, padx=5, pady=5)
    
    # Results listbox to show processing information
    result_frame = tk.Frame(root)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    tk.Label(result_frame, text="Processing Results:").pack(anchor=tk.W)
    
    result_listbox = tk.Listbox(result_frame, width=70, height=15)
    result_listbox.pack(fill=tk.BOTH, expand=True)
    
    # Create a scrollbar for the listbox
    scrollbar = tk.Scrollbar(result_listbox)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_listbox.yview)
    
    # Function to select the parent folder
    def select_folder():
        folder = filedialog.askdirectory(title="Select Parent Folder Containing Subfolders")
        if folder:
            selected_folder.set(folder)
            # Display subfolders in the listbox
            result_listbox.delete(0, tk.END)
            subfolders = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
            result_listbox.insert(tk.END, f"Found {len(subfolders)} subfolders:")
            for subfolder in subfolders:
                result_listbox.insert(tk.END, f"- {subfolder}")
    
    # Function to process files in subfolders
    def process_files():
        folder_path = selected_folder.get()
        
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
                result_listbox.insert(tk.END, f"Created 'rename' folder at: {rename_folder}")
            
            total_renamed = 0
            result_listbox.delete(0, tk.END)
            
            # Get all subfolders from the selected folder
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            
            # Process each subfolder
            for subfolder in subfolders:
                subfolder_path = os.path.join(folder_path, subfolder)
                result_listbox.insert(tk.END, f"Processing subfolder: {subfolder}")
                root.update()
                
                # Find files with "2a_trimmed" in their names
                renamed_in_subfolder = 0
                for root_dir, dirs, files in os.walk(subfolder_path):
                    for file in files:
                        # Check if file contains "2a_trimmed"
                        if "trimmed" in file:
                            file_path = os.path.join(root_dir, file)
                            
                            # Create the new filename by replacing "2a_trimmed" with subfolder name
                            new_filename = subfolder + "_" + file.replace("trimmed", "")
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
                            result_listbox.insert(tk.END, f"  - {file} → {new_filename}")
                            root.update()
                            renamed_in_subfolder += 1
                            total_renamed += 1
                
                result_listbox.insert(tk.END, f"  Found {renamed_in_subfolder} files in '{subfolder}'")
                root.update()
            
            # Show completion message
            if total_renamed > 0:
                result_listbox.insert(tk.END, f"")
                result_listbox.insert(tk.END, f"SUCCESS: Renamed and copied {total_renamed} files to {rename_folder}")
                messagebox.showinfo("Success", f"Successfully renamed and copied {total_renamed} files to {rename_folder}")
                # Open the folder in explorer/finder
                if os.name == 'nt':  # Windows
                    os.startfile(rename_folder)
                elif os.name == 'posix':  # macOS or Linux
                    os.system(f'open "{rename_folder}"')
            else:
                result_listbox.insert(tk.END, f"No files with '2a_trimmed' were found in any subfolder")
                messagebox.showinfo("Information", "No files with '2a_trimmed' were found in any subfolder")
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            result_listbox.insert(tk.END, error_msg)
            messagebox.showerror("Error", error_msg)
    
    # Create buttons for actions
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    select_button = tk.Button(button_frame, text="Select Parent Folder", command=select_folder)
    select_button.pack(side=tk.LEFT, padx=5)
    
    process_button = tk.Button(button_frame, text="Process Files", command=process_files)
    process_button.pack(side=tk.LEFT, padx=5)
    
    # Add status label
    status_label = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()

if __name__ == "__main__":
    rename_files_from_subfolders()
