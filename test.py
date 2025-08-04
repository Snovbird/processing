from common.common import assignval,dropdown,findval,find_folder_path
from extractpng import extractpng
import os
from image_combine import combine_and_resize_images
from photo_carrousel import photo_carrousel
# overlays_path = find_folder_path("2-MARKERS")
# room = "12cage"
# room_options = os.listdir(overlays_path)
imgpath = r"C:\Users\samahalabo\Desktop\0-RECORDINGS\2025-6-25\20250625.mp41\202506251\202506251\(not ready) processed videos1\combined1\png1\1a_20250625_000.png"
# date_today = "20250625"
# cage_number = ''.join(char for char in os.path.splitext(os.path.basename(imgpath))[0][0:2] if char.isdigit()) # extract digits from first two filename characters to get cage number
# imagepath = os.path.join(overlays_path, room,f"cage{cage_number}_{date_today}.png") # f"{width}/cage{cage_number}_{alldates[d]}_{width}.png")

# combined_outputpath = combine_and_resize_images(imgpath,imagepath,output_folder=r"C:\Users\samahalabo\Desktop\0-RECORDINGS\2025-6-25\20250625.mp41\202506251\202506251\(not ready) processed videos1\combined1\png1")

# photo_carrousel(combined_outputpath)
combine_and_resize_images(imgpath, r"C:\Users\samahalabo\Desktop\2-MARKERS\12cage\cage6_20250616.png",output_folder=r"C:\Users\samahalabo\Desktop")
