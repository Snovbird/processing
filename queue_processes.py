# necessary
from common.common import askint,select_video,select_folder,simple_dropdown,custom_dialog,makefolder,msgbox,list_filespaths
import wx,os
# Queue-able processes
from concatenate import concatenate
from extractpng import extractpng
from frameoverlay import overlay_FRAMES
from markersquick import apply_png_overlay
from newtrim import trim_DS_auto
# from photo_carrousel import photo_carrousel
# from image_combine import combine_and_resize_images
functions = [trim_DS_auto,apply_png_overlay,concatenate,extractpng,overlay_FRAMES]
def queue():
    functions_str:list[str] = [str(func).split(" ")[1] for func in functions] #"photo_carrousel","combine_and_resize_images"
    ind = simple_dropdown(functions_str,return_index=True)
    if ind is None:
        return
    sel = functions[ind]
    sel_name = functions_str[ind]
    if not sel:
        return
    # choice= custom_dialog("Select different videos for each process or select same videos for all?","Input Handling",op1="DIFF vids",op2="SAME vids")
    videos = []
    folder_or_file_explorer = custom_dialog("Select files or folders?","Input Handling",op1="Files",op2="Folders")
    selection = True
    if folder_or_file_explorer == "Folders":
        while selection:
            selection = select_folder(f"Select folder. Cancel to stop file explorer loop",path=os.path.dirname(selection) if isinstance(selection,str) else False)
            if selection:
                print(f"{selection=}")
                videos.append(list_filespaths(selection))
    elif folder_or_file_explorer == "Files":
        while selection:
            selection = select_video(f"Select videos. Cancel to stop file explorer loop")
            if selection:
                videos.append(selection)
            # for function in range(how_many_functions):
            #     sel = dropdown(functions)
            #     selected_functions.append(sel)
            #     functions.remove(sel)
    count = 0
    if sel_name == "trim_DS_auto":
        which = simple_dropdown(["DS+","DS-","ALL IN ONE","BOTH SEPARATE"])
        for group in videos:
            sel(group,which=which)
    else:
        for group in videos:
            output_folder = makefolder(group[0],"Processed videos-")
            for vid in group:  
                exec(f"{sel}(vid,output_folder=r'{output_folder}')")
                count +=1
        return count,sel_name
            
if __name__ == "__main__":
    c,sel_name = queue()
    msgbox(f"Successfully used {sel_name} on {c} videos")