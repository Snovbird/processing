from common.common import select_folder,find_folder_path,msgbox,dropdown,list_files,list_folders
import os
import shutil

def main():
    parent = select_folder("Select parent folder",path=find_folder_path("6-GENERATED behavior examples pairs"))
    if not parent:
        return
    sorted_dir7 = find_folder_path("7-SORTED behaviors examples pairs")
    bv_clips_dir = find_folder_path("5-behavior video CLIPS")
    destinations = [folder for folder in os.listdir(bv_clips_dir) if os.path.isdir(os.path.join(bv_clips_dir,folder))]
    # destinations = [os.path.join(sorted_dir7,destination) for destination in destinations.copy()] # behavior names
    dtn = dropdown(choices=destinations,title="Choose destination")
    if not dtn:
        return
    dtn = os.path.join(sorted_dir7,dtn)
    if not os.path.exists:
        os.makedirs(dtn)
    # dtn = select_folder(path=sorted_dir7)

    # The original list comprehension was incorrect. This is a more readable and correct way to achieve the goal.
    # It finds all files in the second level of subdirectories, matching the structure:
    # parent -> folder -> subfolder -> file.ext
    list_of_lists_of_files = []
    for folder_name in os.listdir(parent):
        folder_path = os.path.join(parent, folder_name)
        if os.path.isdir(folder_path):
            # As per the description, each of these folders contains another subfolder.
            for subfolder_name in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    # Collect all file paths from this subfolder.
                    files_in_subfolder = [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
                    if files_in_subfolder:
                        list_of_lists_of_files.append(files_in_subfolder)

    print(list_of_lists_of_files)
    for list_of_files in list_of_lists_of_files:
        for file in list_of_files:
            shutil.move(file,dtn)
            pass
    moved = sum([len(sublist) for sublist in list_of_lists_of_files])

    msgbox(f"Successfully moved {moved} files to {os.path.basename(dtn)}")

if __name__ == "__main__":
    main()

    