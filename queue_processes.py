# necessary
from common.common import askint,select_video,select_folder,dropdown,custom_dialog,makefolder

# Queue-able processes
from concatenate import combine_videos_with_cuda
from extractpng import extractpng
from frameoverlay import overlay_FRAMES
from markersquick import apply_png_overlay
# from photo_carrousel import photo_carrousel
# from image_combine import combine_and_resize_images

def queue():
    functions:list[str] = ["combine_videos_with_cuda","extractpng","overlay_FRAMES","apply_png_overlay",] #"photo_carrousel","combine_and_resize_images"
    sel = dropdown(functions)
    if not sel:
        return
    # choice= custom_dialog("Select different videos for each process or select same videos for all?","Input Handling",op1="DIFF vids",op2="SAME vids")
    videos = []
    selection = True
    while selection:
        selection = select_video(f"Select videos. Cancel to stop loop")
        if selection:
            videos.append(selection)
        # for function in range(how_many_functions):
        #     sel = dropdown(functions)
        #     selected_functions.append(sel)
        #     functions.remove(sel)
    for group in videos:
        output_folder = makefolder(group[0],"Processed videos-")
        for vid in group:  
            exec(f"{sel}(vid, output_folder='{output_folder}')")
            
if __name__ == "__main__":
    queue()