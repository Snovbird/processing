import wx
import os

def combine_and_resize_images(photo1_path, photo2_path, output_folder=None,target_width=1024, target_height=768, ):
    """
    Combines two PNG images (one transparent) and resizes them.

    Args:
        photo1_path (str): Path to the base PNG image.
        photo2_path (str): Path to the transparent overlay PNG image.
        output_folder (str): Path to save the combined and resized image.
        target_width (int): Desired width for the output image.
        target_height (int): Desired height for the output image.
    """
    app = wx.App(False) # Initialize wxWidgets application
    count = 0
    if not output_folder:
        output_folder = os.path.dirname(photo1_path)
    full_output_path = os.path.join(output_folder, f'combined.png')
    while os.path.exists(full_output_path):
        count += 1
        full_output_path = os.path.join(output_folder, f'combined{count}.png')

    try:
        # Load the base image (photo1)
        img1 = wx.Image(photo1_path, wx.BITMAP_TYPE_PNG)
        if not img1.IsOk():
            print(f"Error: Could not load base image from {photo1_path}")
            return

        # Load the overlay image (photo2)
        img2 = wx.Image(photo2_path, wx.BITMAP_TYPE_PNG)
        if not img2.IsOk():
            print(f"Error: Could not load overlay image from {photo2_path}")
            return

        # Resize the base image to target dimensions
        img1 = img1.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)

        # Resize the overlay image to target dimensions
        img2 = img2.Scale(target_width, target_height, wx.IMAGE_QUALITY_HIGH)

        # Convert images to bitmaps for drawing
        bmp1 = img1.ConvertToBitmap()
        bmp2 = img2.ConvertToBitmap()

        # Create a memory DC to draw on
        dc = wx.MemoryDC()
        dc.SelectObject(bmp1)  # Select bmp1 as the base to draw on

        # Draw bmp2 (overlay) onto bmp1 at position (0,0)
        # The last argument (True) indicates that the mask (transparency) should be used.
        dc.DrawBitmap(bmp2, 0, 0, True)        # Deselect the bitmap
        dc.SelectObject(wx.NullBitmap)

        # Save the combined image
        bmp1.SaveFile(output_folder, wx.BITMAP_TYPE_PNG)
        print(f"Combined and resized image saved to: {output_folder}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'app' in locals() and app:
            app.Destroy()


combine_and_resize_images(r"C:\Users\samahalabo\Desktop\.SNAPSHOTS (images)\1_7-trim(207-500)_1-04.png",r"C:\Users\samahalabo\Desktop\.SNAPSHOTS (images)\cage6_06-16.png",r"C:\Users\samahalabo\Desktop\.SNAPSHOTS (images)")