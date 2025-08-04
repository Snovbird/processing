from PIL import Image, ImageEnhance
import os

def combine_and_resize_images(photo1_path, photo2_path, output_folder=None, 
                            target_width=1024, target_height=768, overlay_opacity=1.0):
    """
    Combines two PNG images with advanced transparency handling.
    
    Args:
        photo1_path (str): Path to the base PNG image.
        photo2_path (str): Path to the transparent overlay PNG image.
        output_folder (str): Path to save the combined and resized image.
        target_width (int): Desired width for the output image.
        target_height (int): Desired height for the output image.
        overlay_opacity (float): Opacity of the overlay image (0.0 to 1.0).
    
    Returns:
        str: Path to the saved combined image.
    """
    count = 0
    if not output_folder:
        output_folder = os.path.dirname(photo1_path)
    
    full_output_path = os.path.join(output_folder, 'combined.png')
    while os.path.exists(full_output_path):
        count += 1
        full_output_path = os.path.join(output_folder, f'combined{count}.png')

    try:
        # Load and convert images to RGBA
        base_img = Image.open(photo1_path).convert("RGBA")
        overlay_img = Image.open(photo2_path).convert("RGBA")
        
        # Resize images with high quality resampling
        base_img = base_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        overlay_img = overlay_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Adjust overlay opacity if needed
        if overlay_opacity < 1.0:
            # Split the overlay into RGB and Alpha channels
            r, g, b, a = overlay_img.split()
            # Reduce alpha channel by opacity factor
            a = ImageEnhance.Brightness(a).enhance(overlay_opacity)
            overlay_img = Image.merge("RGBA", (r, g, b, a))
        
        # Combine images using alpha compositing
        result = Image.alpha_composite(base_img, overlay_img)
        
        # Save with optimization
        result.save(full_output_path, "PNG", optimize=True, compress_level=6)
        print(f"Combined and resized image saved to: {full_output_path}")
        
        return full_output_path

    except FileNotFoundError as e:
        print(f"Error: Image file not found - {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == "__main__":
    from common.common import select_anyfile,select_folder
    combine_and_resize_images(select_anyfile()[0],select_anyfile()[0],select_folder())