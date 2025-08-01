from cagename import name_cages
from concatenate import combine_videos_with_cuda,group_files_by_digits
from common.common import select_folder,clear_gpu_memory,get_date_mmdd,find_folder_path,findval,assignval,makefolder,error
from markersquick import apply_png_overlay
import os, shutil
from frameoverlay import overlay_FRAMES

def process_folder():
    """Process a videos of video recordings by naming cages and concatenating videos."""
    # Select the folder to process
    folder_path = select_folder("Select the folder containing the recordings to process",path=find_folder_path("0-RECORDINGS"))
    if not folder_path:
        return
    
    # First, name the cages in the selected folder
    name_cages(folder_path)
    
    # Get all video files in the folder
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    # Group files by their digit sequences for concatenation
    grouped_files = group_files_by_digits(files)
    
    if not grouped_files:
        print("No files found that can be grouped for concatenation.")
        return
        
    # Convert relative paths to absolute paths
    grouped_files = [[os.path.join(folder_path, file) for file in group] for group in grouped_files]
    
    # Create output videos for concatenated videos
    from common.common import makefolder
    concatenation_output_folder = makefolder(grouped_files[0][0], foldername='(not ready) processed videos')
    
    # Concatenate each group of videos
    for group in grouped_files:
        combine_videos_with_cuda(group, concatenation_output_folder)
        if clear_gpu_memory():
            pass
    did_break = None


    for count, concatenated_video_path in enumerate([os.path.join(concatenation_output_folder, basename) for basename in sorted(os.listdir(concatenation_output_folder)) if os.path.isfile(os.path.join(concatenation_output_folder, basename))]):
        if count == 0:
            marked_outputs_folder = makefolder(concatenated_video_path, foldername='marked')
        if apply_png_overlay(concatenated_video_path, # if statement is to check whether the transparent overlay images exist; if DNE -> returns string "No overlay png Error"
                          marked_outputs_folder,
                          cage_number=''.join(char for char in os.path.splitext(os.path.basename(concatenated_video_path))[0][0:2] if char.isdigit()),
                          thedate=get_date_mmdd(),
                          overlays_path=find_folder_path("2-MARKERS")
                          ) == "Error: No overlay png":
            did_break = True
            break
        if clear_gpu_memory():
            pass
    else:
        for count, marked_vid_path in enumerate([os.path.join(marked_outputs_folder, basename) for basename in sorted(os.listdir(marked_outputs_folder)) if os.path.isfile(os.path.join(marked_outputs_folder, basename))]):
            if count == 0:
                frameoverlay_output_folder = makefolder(marked_vid_path, foldername='frameoverlay-')
            if not overlay_FRAMES(marked_vid_path,
                            frameoverlay_output_folder,
                            ):
                error(f"Overlay error for:\n{marked_vid_path}\ninto {frameoverlay_output_folder}") # error if does not return output path
            
            if clear_gpu_memory():
                pass
        new_name = os.path.join(os.path.dirname(frameoverlay_output_folder),"VIDEOS READY FOR ANALYSIS")
        final_output_folder = makefolder(folder_path,foldername="VIDEOS READY FOR ANALYSIS-")    
        for file in [os.path.join(frameoverlay_output_folder, basename) for basename in sorted(os.listdir(frameoverlay_output_folder)) if os.path.isfile(os.path.join(frameoverlay_output_folder, basename))]:
            shutil.move(file,final_output_folder)
        
        os.remove(concatenation_output_folder)
    if did_break:
        emergency_overlay_maker()
        os.remove(concatenation_output_folder)

def emergency_overlay_maker():
    # shutil.copy(photoshop project)
    pass

def photo_carrousel(photo1_path):
    import wx

    app = wx.App(False)
    frame = wx.Frame(None, title="Photo Carousel", size=(1024+40, 768+40))

    # Load the base image (photo1)
    img1 = wx.Image(photo1_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

    # Create a memory DC to draw on
    dc = wx.MemoryDC()
    dc.SelectObject(img1)  # Select img1 as the base to draw on

    # Deselect the bitmap
    dc.SelectObject(wx.NullBitmap)

    # Create a static bitmap to display the result
    wx.StaticBitmap(frame, -1, img1, (0, 0), (img1.GetWidth(), img1.GetHeight()))

    frame.Show()
    app.MainLoop()    
    
    def on_button_click(event):
        button = event.GetEventObject()
        print(f"Button '{button.GetLabel()}' clicked!")
        frame.Close()

    # Create a panel to hold the buttons
    panel = wx.Panel(frame)
    
    # Create a sizer for the panel
    sizer = wx.BoxSizer(wx.VERTICAL)
    
    # Add the image to the sizer
    sizer.Add(wx.StaticBitmap(panel, -1, img1), 0, wx.ALL | wx.CENTER, 10)

    # Create buttons
    button1 = wx.Button(panel, label="Button 1")
    button2 = wx.Button(panel, label="Button 2")

    # Bind buttons to event handler
    button1.Bind(wx.EVT_BUTTON, on_button_click)
    button2.Bind(wx.EVT_BUTTON, on_button_click)

    # Add buttons to sizer
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)
    button_sizer.Add(button1, 0, wx.ALL, 5)
    button_sizer.Add(button2, 0, wx.ALL, 5)
    sizer.Add(button_sizer, 0, wx.CENTER)

    panel.SetSizer(sizer)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    # process_folder()
    process_folder()