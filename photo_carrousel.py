import wx
from common.common import select_anyfile

def photo_carrousel(photo1_path):
    app = wx.App(False)
    frame = wx.Frame(None, title="Photo Carousel", size=(1024 + 40, 768 + 40))
    selection = [None]  # Use a list to make it mutable for the nested function
    # It's best practice to put all controls on a panel
    panel = wx.Panel(frame)

    # Load the base image
    try:
        # Use wx.BITMAP_TYPE_ANY to automatically detect file type
        img1_bitmap = wx.Image(photo1_path[0], wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    except Exception as e:
        wx.MessageBox(f"Failed to load image: {e}", "Error", wx.OK | wx.ICON_ERROR)
        frame.Destroy()
        return None

    def on_button_click(event):
        button = event.GetEventObject()
        # print(f"Button '{button.GetLabel()}' clicked!")
        selection[0] = button.GetLabel()  # Modify the list element
        frame.Close()

    # Create a sizer for the panel to arrange widgets vertically
    main_sizer = wx.BoxSizer(wx.VERTICAL)

    # Add the image to the sizer
    image_widget = wx.StaticBitmap(panel, -1, img1_bitmap)
    main_sizer.Add(image_widget, 0, wx.ALL | wx.CENTER, 10)

    # Create a horizontal sizer for the buttons
    button_sizer = wx.BoxSizer(wx.HORIZONTAL)

    # Create buttons
    button1 = wx.Button(panel, label="STOP markers NOT aligned")
    button2 = wx.Button(panel, label="All good go to next image")

    # Bind buttons to the event handler
    button1.Bind(wx.EVT_BUTTON, on_button_click)
    button2.Bind(wx.EVT_BUTTON, on_button_click)

    # Add buttons to the horizontal sizer
    button_sizer.Add(button1, 0, wx.ALL, 5)
    button_sizer.Add(button2, 0, wx.ALL, 5)

    # Add the button sizer to the main vertical sizer
    main_sizer.Add(button_sizer, 0, wx.CENTER)

    # Set the sizer for the panel and fit the layout
    panel.SetSizer(main_sizer)
    panel.Layout()

    # Show the frame and start the application's main event loop
    frame.Show()
    app.MainLoop()
    return selection[0]  # Return the actual selection


def main():
    photo1 = select_anyfile()
    if photo1:  # Check if a file was selected
        print(photo_carrousel(photo1))

if __name__ == "__main__":
    main()