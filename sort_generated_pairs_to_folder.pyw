from common.common import select_folder,find_folder_path,msgbox,dropdown,list_files,list_folders,list_folderspaths
import os
import shutil

def main():
    # parent = select_folder("Select parent folder",path=find_folder_path("6-GENERATED EXAMPLES"))
    # if not parent:
    #     return
    successes = []
    dir7 = find_folder_path("7-SORTED")
    destinations = list_folders(dir7)

    parents_in_parent = [folderpath for folderpath in list_folderspaths(find_folder_path("6-GENERATED EXAMPLES")) if len(list_folders(folderpath)) > 0]
    for n, parent in enumerate(parents_in_parent): # parents inside bigger parent folder "6-GENERATED EXAMPLES"
        if os.path.basename(parent) in destinations:
            dtn = os.path.join(dir7,os.path.basename(parent))
        else:
            dtn = None
        msg = move_files_in_subdir(parent,dtn)
        if not msg:
            return
        successes.append(msg)
        
    msgbox("Successfully moved:\n\n"+"\n".join(successes),"Success")

def move_files_in_subdir(parent_dir=None,dtn=None):
    if not dtn:
        bv_clips_dir:str = find_folder_path("5-clips")
        destinations:list[str] = list_folders(bv_clips_dir)
        dtn:str = dropdown(choices=destinations,title=f"Choose destination for {os.path.basename(parent_dir)}")
        sorted_dir7 = find_folder_path("7-SORTED")
        dtn = os.path.join(sorted_dir7,dtn)
        if not dtn:
            return
    
    if not os.path.exists(dtn):
        os.makedirs(dtn)
    # dtn = select_folder(path=sorted_dir7)

    # The original list comprehension was incorrect. This is a more readable and correct way to achieve the goal.
    # It finds all files in the second level of subdirectories, matching the structure:
    # parent -> folder -> subfolder -> file.ext
    list_of_lists_of_files = []

    inside_parent = os.listdir(parent_dir)
    if len(inside_parent) == 0:
        shutil.rmtree(parent_dir)
        os.makedirs(parent_dir)
        return ''
    for folder_name in inside_parent:
        folder_path = os.path.join(parent_dir, folder_name)
        if os.path.isdir(folder_path):
            # As per the description, each of these folders contains another subfolder.
            for subfolder_name in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    # Collect all file paths from this subfolder.
                    files_in_subfolder = [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
                    if len(files_in_subfolder) == 0:
                        continue 
                    if files_in_subfolder:
                        list_of_lists_of_files.append(files_in_subfolder)
    
    if len(list_of_lists_of_files) == 0:
        shutil.rmtree(parent_dir)
        os.makedirs(parent_dir)
        return f"0 files to {os.path.basename(dtn)}"
    for list_of_files in list_of_lists_of_files:
        for file in list_of_files:
            shutil.move(file,dtn)
    shutil.rmtree(parent_dir)
    os.makedirs(parent_dir)
    moved:int = sum([len(sublist) for sublist in list_of_lists_of_files])

    return f"{moved} files to {os.path.basename(dtn)}"

if __name__ == "__main__":
    main()

    