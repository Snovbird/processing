from common.common import *
from markersquick import find_overlay_path
from image_combine import combine_and_resize_images
import os

def names():
    parent_folder = r"C:\Users\samahalabo\Desktop\4-detector\1.ANNOTATED imgs and json\2048x1536-lights+rats+levers"
    for imgfolder in list_folderspaths(parent_folder):
        overlaid = os.path.join(imgfolder,"overlaid")

        for img in list_filespaths(overlaid):
            img_name = img.replace("_combined","")
            os.rename(img,img_name)


def main():
    # Select the first image (base) and the second image (overlay)
    # parent_folder = select_folder("Select the folder containing the images")
    parent_folder = r"C:\Users\samahalabo\Desktop\4-detector\1.ANNOTATED imgs and json\2048x1536-lights+rats+levers"
    for imgfolder in list_folderspaths(parent_folder):
        overlaid = os.path.join(imgfolder,"overlaid")
        if not os.path.exists(overlaid):
            overlaid = makefolder(imgfolder,foldername="overlaid",start_at_1=False)

        for img in list_filespaths(imgfolder):
            overlaid_name_check = os.path.basename(img).replace(".png","_combined.png")
            if overlaid_name_check in list_files(overlaid):
                continue
            parts = os.path.basename(img).split("-")
            cage_number = parts[0]
            date = parts[1]
            room = "OPTO-ROOM (12 cages)"
            overlay = find_overlay_path(os.path.basename(img), room=room)

            combine_and_resize_images(img,overlay,overlaid,target_width=2048,target_height=1536)
            
main()