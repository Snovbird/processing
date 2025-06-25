import wx
import os
from PIL import Image

def displace_left(image):
    """Displaces a PIL image 1 pixel to the left and fills with transparency"""
    width, height = image.size
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    pixel_data = image.load()
    new_pixel_data = new_img.load()
    
    for y in range(height):
        for x in range(width - 1):
            new_pixel_data[x, y] = pixel_data[x + 1, y]
    
    return new_img

def displace_right(image):
    """Displaces a PIL image 1 pixel to the right and fills with transparency"""
    width, height = image.size
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    pixel_data = image.load()
    new_pixel_data = new_img.load()
    
    for y in range(height):
        for x in range(1, width):
            new_pixel_data[x, y] = pixel_data[x - 1, y]
    
    return new_img

def displace_up(image):
    """Displaces a PIL image 1 pixel upward and fills with transparency"""
    width, height = image.size
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    pixel_data = image.load()
    new_pixel_data = new_img.load()
    
    for y in range(height - 1):
        for x in range(width):
            new_pixel_data[x, y] = pixel_data[x, y + 1]
    
    return new_img

def displace_down(image):
    """Displaces a PIL image 1 pixel downward and fills with transparency"""
    width, height = image.size
    new_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    pixel_data = image.load()
    new_pixel_data = new_img.load()
    
    for y in range(1, height):
        for x in range(width):
            new_pixel_data[x, y] = pixel_data[x, y - 1]
    
    return new_img

def pil_to_wx(pil_image):
    """Convert PIL Image to wx.Bitmap with proper transparency handling"""
    width, height = pil_image.size
    
    # Convert to RGBA if not already
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA') [[1]]
    
    # Extract RGB and Alpha channels
    rgb_data = pil_image.convert('RGB').tobytes()
    alpha_data = pil_image.getchannel('A').tobytes()
    
    # Create wx.Image and set RGB and Alpha data
    wx_image = wx.Image(width, height)
    wx_image.SetData(rgb_data)
    wx_image.SetAlpha(alpha_data)
    
    return wx.Bitmap(wx_image)

class ImageDisplacerFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ImageDisplacerFrame, self).__init__(parent, title=title, size=(800, 600))
        
        # Initialize variables
        self.foreground_image = None  # PIL image
        self.foreground_path = None   # Path to save later
        self.background_image = None  # PIL image
        self.panel = wx.Panel(self)
        
        # Load images
        if not self.get_foreground_image():
            self.Close()
            return
            
        if not self.get_background_image():
            self.Close()
            return
        
        # Create a static bitmap to display the composite image
        self.image_display = wx.StaticBitmap(self.panel)
        
        # Set up sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.image_display, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        
        # Update display
        self.update_display()
        
        # Bind key events
        self.panel.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        # Make sure panel can receive keyboard focus
        self.panel.SetFocus()
        
        # Center the frame
        self.Centre()
    
    def get_foreground_image(self):
        """Open file dialog to get the foreground PNG image"""
        wildcard = "PNG files (*.png)|*.png"
        dialog = wx.FileDialog(None, "Choose foreground PNG image", wildcard=wildcard, style=wx.FD_OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            self.foreground_path = dialog.GetPath()
            try:
                self.foreground_image = Image.open(self.foreground_path).convert("RGBA")
                dialog.Destroy()
                return True
            except Exception as e:
                wx.MessageBox(f"Error opening image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
        return False
        
    def get_background_image(self):
        """Open file dialog to get the background image"""
        wildcard = "Image files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp"
        dialog = wx.FileDialog(None, "Choose background image", wildcard=wildcard, style=wx.FD_OPEN)
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                self.background_image = Image.open(dialog.GetPath()).convert("RGBA")
                
                # Resize background to match foreground dimensions if needed
                if self.background_image.size != self.foreground_image.size:
                    self.background_image = self.background_image.resize(self.foreground_image.size)
                    
                dialog.Destroy()
                return True
            except Exception as e:
                wx.MessageBox(f"Error opening image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()
        return False
        
    def update_display(self):
        """Update displayed image by combining background and foreground"""
        if self.foreground_image and self.background_image:
            # Create a composite image
            composite = self.background_image.copy()
            composite.paste(self.foreground_image, (0, 0), self.foreground_image)
            
            # Convert to wx.Bitmap and display
            bitmap = pil_to_wx(composite)
            self.image_display.SetBitmap(bitmap)
            
            # Adjust frame size if needed
            self.SetClientSize(bitmap.GetWidth(), bitmap.GetHeight())
            self.Layout()
    
    def on_key_down(self, event):
        """Handle key press events"""
        key_code = event.GetKeyCode()
        
        if key_code == wx.WXK_LEFT:
            self.foreground_image = displace_left(self.foreground_image)
            self.update_display()
        elif key_code == wx.WXK_RIGHT:
            self.foreground_image = displace_right(self.foreground_image)
            self.update_display()
        elif key_code == wx.WXK_UP:
            self.foreground_image = displace_up(self.foreground_image)
            self.update_display()
        elif key_code == wx.WXK_DOWN:
            self.foreground_image = displace_down(self.foreground_image)
            self.update_display()
        elif key_code == wx.WXK_RETURN:
            self.save_and_exit()
        else:
            event.Skip()
            
    def save_and_exit(self):
        """Save the modified foreground image and exit"""
        try:
            # Get output path, default to original path
            output_dialog = wx.FileDialog(
                self, "Save image", os.path.dirname(self.foreground_path),
                os.path.basename(self.foreground_path),
                "PNG files (*.png)|*.png", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
            
            if output_dialog.ShowModal() == wx.ID_OK:
                save_path = output_dialog.GetPath()
                self.foreground_image.save(save_path, "PNG")
                output_dialog.Destroy()
                self.Close()
            else:
                output_dialog.Destroy()
        except Exception as e:
            wx.MessageBox(f"Error saving image: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

# Main application
class ImageDisplacerApp(wx.App):
    def OnInit(self):
        frame = ImageDisplacerFrame(None, "Image Displacer")
        frame.Show()
        return True

if __name__ == "__main__":
    app = ImageDisplacerApp()
    app.MainLoop()
