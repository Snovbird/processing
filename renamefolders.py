import os
from common.common import select_folder,askstring,custom_dialog
import shutil

def rename_files_from_subfolders():
    # Create the main window
    #     
    # Variable to store selected folder path
    selected_folder = select_folder(
        title="Select parent folder",
    )
    if not selected_folder:
        return
    answer = custom_dialog("Enter a string to remove?","Remove in name?",op1='yes',op2='no')
    
    if answer == 'yes':
        strtoremove = askstring( "Enter a string to remove in filenames:","To remove")
    else:
        strtoremove = ''
    # Function to process files in subfolders
    def process_files(folder_path):
        
        if not folder_path:
            print("Warning", "Please select a parent folder first!")
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
                for root_dir, dirs, files in os.walk(subfolder_path):
                    for file in files:
                        # Check if file contains "2a_trimmed"
                        if answer and strtoremove in file:
                            file_path = os.path.join(root_dir, file)
                            
                            # Create the new filename by replacing "2a_trimmed" with subfolder name
                            new_filename = subfolder + "_" + file.replace(strtoremove, "")
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

                        else:
                            file_path = os.path.join(root_dir, file)
                            
                            # Get the file extension
                            _, ext = os.path.splitext(file)
                            
                            # Create the new filename as subfolder_counter.ext
                            counter = 1
                            new_filename = f"{subfolder}_{counter}{ext}"
                            new_path = os.path.join(rename_folder, new_filename)
                            
                            # Increment counter until we find an unused filename
                            while os.path.exists(new_path):
                                counter += 1
                                new_filename = f"{subfolder}_{counter}{ext}"
                                new_path = os.path.join(rename_folder, new_filename)
                            
                            # Copy the file to the rename folder with new name
                            shutil.copy2(file_path, new_path)
                            total_renamed += 1

            
            # Show completion message
            if total_renamed > 0:
                print("Success", f"Successfully renamed and copied {total_renamed} files to {rename_folder}")
                # Open the folder in explorer/finder
                if os.name == 'nt':  # Windows
                    os.startfile(rename_folder)
            else:
                print("Information", "No files with were found in any subfolder")
                
        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            print("Error:", error_msg)
    process_files(selected_folder)

if __name__ == "__main__":
    rename_files_from_subfolders()