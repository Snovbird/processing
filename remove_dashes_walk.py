import os, shutil
from common.common import select_folder, msgbox,error

def file_walk_renamer(folder):
    """
    walks through all files and directories in a folder
    """
    renamed = 0
    
    # First, collect all directories and files that need renaming
    items_to_rename = []
    
    for root, dirs, files in os.walk(folder):
        # Collect directories (we'll rename them in reverse order later)
        for dir_name in dirs:
            if "_" in dir_name:
                full_dir_path = os.path.join(root, dir_name)
                new_dir_name = dir_name.replace("_", "-")
                new_full_path = os.path.join(root, new_dir_name)
                items_to_rename.append(('dir', full_dir_path, new_full_path, dir_name, new_dir_name))
        
        # Collect files
        for file in files:
            if "_" in file:
                full_file_path = os.path.join(root, file)
                new_file_name = file.replace("_", "-")
                new_full_path = os.path.join(root, new_file_name)
                items_to_rename.append(('file', full_file_path, new_full_path, file, new_file_name))
    
    # Sort directories by depth (deepest first) to avoid path conflicts
    dirs_to_rename = [item for item in items_to_rename if item[0] == 'dir']
    files_to_rename = [item for item in items_to_rename if item[0] == 'file']
    
    # Sort directories by path length (deepest first)
    dirs_to_rename.sort(key=lambda x: len(x[1]), reverse=True)
    
    # Rename directories first (deepest first)
    for item_type, old_path, new_path, old_name, new_name in dirs_to_rename:
        try:
            print(f"Renaming directory: {old_name} → {new_name}")
            os.rename(old_path, new_path)
            renamed += 1
        except OSError as e:
            error(f"Error renaming directory {old_name}: {e}")
    
    # Then rename files
    for item_type, old_path, new_path, old_name, new_name in files_to_rename:
        try:
            print(f"Renaming file: {old_name} → {new_name}")
            os.rename(old_path, new_path)
            renamed += 1
        except OSError as e:
            error(f"Error renaming file {old_name}: {e}")
    
    return renamed

# Usage
if __name__ == "__main__":
    folder_path = select_folder("Enter folder path: ").strip().strip('"\'')
    c = file_walk_renamer(folder_path)

    msgbox(f"Renamed {c} items (files and directories)")