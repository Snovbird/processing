import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    """Opens a dialog for the user to select a folder."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    folder_path = filedialog.askdirectory(
        title="Select a folder containing subfolders to rename"
    )
    
    if not folder_path:
        print("No folder selected. Exiting...")
        return None
    
    return folder_path

def rename_subfolders(parent_dir, recursive=True):
    """
    Renames all subfolders in the given directory, replacing underscores with dashes.
    
    Args:
        parent_dir: The parent directory containing subfolders to rename.
        recursive: Whether to recursively rename subfolders of subfolders.
    
    Returns:
        Number of folders renamed.
    """
    if not os.path.exists(parent_dir):
        print(f"Error: The directory '{parent_dir}' does not exist.")
        return 0
    
    renamed_count = 0
    errors = []
    
    try:
        # Get all directories and subdirectories
        all_dirs = []
        if recursive:
            for root, dirs, _ in os.walk(parent_dir):
                for dir_name in dirs:
                    if '_' in dir_name:
                        full_path = os.path.join(root, dir_name)
                        all_dirs.append(full_path)
        else:
            # Only get immediate subdirectories
            for item in os.listdir(parent_dir):
                full_path = os.path.join(parent_dir, item)
                if os.path.isdir(full_path) and '_' in item:
                    all_dirs.append(full_path)
        
        # Sort directories by depth (deepest first) to avoid path issues
        all_dirs.sort(key=lambda x: x.count(os.sep), reverse=True)
        
        # Rename directories
        for dir_path in all_dirs:
            dir_name = os.path.basename(dir_path)
            parent_path = os.path.dirname(dir_path)
            new_name = dir_name.replace('_', '-')
            new_path = os.path.join(parent_path, new_name)
            
            try:
                os.rename(dir_path, new_path)
                print(f"Renamed: '{dir_path}' to '{new_path}'")
                renamed_count += 1
            except PermissionError:
                errors.append(f"Permission denied to rename '{dir_path}'")
            except FileExistsError:
                errors.append(f"Cannot rename '{dir_name}' to '{new_name}' as it already exists")
            except Exception as e:
                errors.append(f"Error renaming '{dir_path}': {str(e)}")
                
    except PermissionError:
        print(f"Error: Permission denied to access '{parent_dir}'.")
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 0
    
    # Display any errors
    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"- {error}")
    
    return renamed_count

def main():
    # Get the parent directory from the user
    parent_dir = select_folder()
    if not parent_dir:
        return
    
    # Ask if the user wants recursive renaming
    root = tk.Tk()
    root.withdraw()
    recursive = messagebox.askyesno("Recursive Renaming", 
                                   "Do you want to rename subfolders within subfolders as well?")
    
    # Rename subfolders
    renamed_count = rename_subfolders(parent_dir, recursive)
    
    # Show completion message
    if renamed_count > 0:
        messagebox.showinfo("Renaming Complete", 
                           f"Successfully renamed {renamed_count} folder(s).\n"
                           f"All underscores were replaced with dashes.")
    else:
        messagebox.showinfo("Renaming Complete", 
                           "No folders were renamed. Either there were no subfolders with underscores or errors occurred.")

if __name__ == "__main__":
    main()
