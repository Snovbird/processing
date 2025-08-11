import os
from markersquick import apply_png_overlay
from common.common import select_video,askint,makefolder,find_folder_path,assignval,askstring,findval

def main():
    sets = askint(msg="How many different cages for same date? ",title="Iterations")
    all_sets_vids = [select_video(title=f"Select videos for set {i+1} of {sets}") for i in range(sets)]
    the_date = askstring(msg="Enter the date formatted as MM-DD:",title="Enter Date",fill=findval("last_used_date"))
    overlays_path = os.path.join(find_folder_path("2-markers"),"OPTO-ROOM (12 cages)")
    for a_set in all_sets_vids:
        output_path = makefolder(a_set[0],"marked")
        cage_number=''.join(char for char in os.path.splitext(os.path.basename(a_set[0]))[0] if char.isdigit())
        for vid in a_set:
            apply_png_overlay(video_path=vid, cage_number=cage_number,width=2048,thedate=the_date,overlays_path=overlays_path,output_path=output_path)
    assignval("last_used_date", the_date )

main()
