import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess
import platform

def resize_folder(input_list, width, input_path):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    """
    # Create a new folder for resized videos
    resized_folder_name = f"{input_path.split('/')[-2]}_resized_{width}"
    resized_folder_path = os.path.join("C:/Users/Labo Samaha/Desktop/.LabGym/1) Processed videos/", resized_folder_name)

    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        messagebox.showerror("ERROR", f"DELETE the folder called '{resized_folder_name}'")
        os.startfile("C:/Users/Labo Samaha/Desktop/.LabGym/1) Processed videos/")
        return None
    if not os.path.exists(resized_folder_path):
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
    
    for input_path in input_list:
        # Skip non-video files
        _, ext = os.path.splitext(input_path.lower())
        if ext not in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
            continue
            
        # Get the filename of the input video
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        # Set output path in the new folder
        output_path = os.path.join(resized_folder_path, f"{file_name}.mp4")
        
        try:
            # FFmpeg command to resize the video proportionally using GPU acceleration
            cmd = [
                "ffmpeg",
                "-hwaccel", "cuda",
                "-hwaccel_output_format", "cuda",
                "-i", input_path,
                "-vf", f"scale_cuda={width}:-2",
                "-c:v", "h264_nvenc",
                "-y",
                "-an",
                output_path
            ]
            
            print(f"Resizing video: {input_path}")
            subprocess.run(cmd, check=True)
            print(f"Resizing completed successfully! Saved to: {output_path}")
        
        except subprocess.CalledProcessError as e:
            print(f"Error during resizing: {e}")
        except FileNotFoundError:
            print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
            return None
    
    return resized_folder_path

def resize_single(input_path, width):
    """
    Resize a video proportionally using FFmpeg with NVIDIA GPU acceleration.
    """
    # Get the directory and filename of the input video
    file_dir = os.path.dirname(input_path)
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join("C:/Users/Labo Samaha/Desktop/.LabGym/1) Processed videos/", f"{file_name}_RESIZED{width}.mp4")

    try:
        # FFmpeg command to resize the video proportionally using GPU acceleration
        cmd = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-hwaccel_output_format", "cuda",
            "-i", input_path,
            "-vf", f"scale_cuda={width}:-2",
            "-c:v", "h264_nvenc",
            "-c:a", "copy",
            "-y",
            "-an",
            output_path
        ]
        
        print("Starting video resizing...")
        subprocess.run(cmd, check=True)
        print(f"Resizing completed successfully! Resized video saved to: {output_path}")
        
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during resizing: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def clear_gpu_memory():
    try:
        # Reset GPU clocks temporarily to help clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False
    
def main():
    # Initialize tkinter with a single root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window but keep it as the root
    
    # Use askopenfilename to select a file
    try:
        file_path = filedialog.askopenfilename(
            title="SELECT VIDEO - option to resize one or all videos in folder",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")],
            initialdir="C:/Users/Labo Samaha/Desktop/.LabGym/0) RAW videos"
        )
    except: #C:/Users/Labo Samaha/Desktop/.LabGym/0) RAW videos DNE 
        file_path = filedialog.askopenfilename(
            title="SELECT VIDEO - option to resize one or all videos in folder",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.webm")]
        )
    
    if not file_path:
        messagebox.showerror("ERROR", "No file selected")
        root.destroy()
        return
    
    # Ask the user for the desired width
    width = simpledialog.askinteger("Input Width", "Enter the desired width (e.g., 1280):")
    if not width:
        print("No width provided. Exiting...")
        root.destroy()
        return
        
    if width % 32 != 0:
        messagebox.showerror("ERROR", "Width MUST be a multiple of 32\nExamples: 1920, 1280, 1024, 480")
        root.destroy()
        return
    
    # ---- SELECTION UI INTEGRATED HERE ----
    # Variable to store the selected choice
    chosen_option = [None]
    
    # Create a new window for selection
    selection_window = tk.Toplevel(root)
    selection_window.title("Selection")
    selection_window.geometry("300x150")
    
    # Center the window
    width_px = 300
    height_px = 150
    x = (selection_window.winfo_screenwidth() // 2) - (width_px // 2)
    y = (selection_window.winfo_screenheight() // 2) - (height_px // 2)
    selection_window.geometry(f"{width_px}x{height_px}+{x}+{y}")
    
    # Function to handle button clicks
    def handle_choice(choice):
        chosen_option[0] = choice
        selection_window.destroy()

    # Add a title label
    title_label = tk.Label(selection_window, text="Choose selection:", font=("Arial", 14))
    title_label.pack(pady=(10, 20))

    # Create frame for buttons
    button_frame = tk.Frame(selection_window)
    button_frame.pack()

    # Create buttons
    file_button = tk.Button(
        button_frame, 
        text="Selected FILE", 
        command=lambda: handle_choice("single"), 
        width=12
    )
    file_button.grid(row=0, column=0, padx=10)

    folder_button = tk.Button(
        button_frame, 
        text="ENTIRE FOLDER", 
        command=lambda: handle_choice("folder"), 
        width=12
    )
    folder_button.grid(row=0, column=1, padx=10)
    
    # Wait for selection window to close before continuing
    root.wait_window(selection_window)
    # ---- END OF SELECTION UI ----
    
    # Check if a choice was made
    if chosen_option[0] is None:
        messagebox.showerror("ERROR", "No option selected")
        root.destroy()
        return
    
    # Process based on user's choice
    output_single = None
    resized_folder = None
    
    if chosen_option[0] == "single":
        # Resize the single selected file
        output_single = resize_single(file_path, width)
    elif chosen_option[0] == "folder":
        # Process the entire folder
        folder_path = os.path.dirname(file_path)
        # Get all files in the folder
        allfiles = []
        for file in os.listdir(folder_path):
            file_full_path = os.path.join(folder_path, file)
            if os.path.isfile(file_full_path):
                allfiles.append(file_full_path)
        resized_folder = resize_folder(allfiles, width,file_path)
    # NOW it's safe to destroy the root window (after all tkinter operations)
    root.destroy()
    # Open the folder containing the resized videos
    
    if resized_folder:
        os.startfile(resized_folder)
    elif output_single:
        os.startfile("C:/Users/Labo Samaha/Desktop/.LabGym/1) Processed videos/")

if __name__ == "__main__":
    main()
