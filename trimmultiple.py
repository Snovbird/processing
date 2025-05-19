import tkinter as tk
from tkinter import simpledialog, filedialog
import os
import subprocess
import platform
from tkinter import messagebox

def format_time_input(time_input):
    """
    Format the time input to HH:MM:SS.
    
    Args:
        time_input (str): The input time as a string without colons.
    
    Returns:
        str: Formatted time as HH:MM:SS.
    """
    time_input = time_input.strip()
    
    if time_input.isdigit():
        time_input = time_input.zfill(6)
        return f"{time_input[:-4]}:{time_input[-4:-2]}:{time_input[-2:]}"
    else:
        return time_input  # Return the original input if it's not valid

def clear_gpu_memory():
    try:
        # Reset GPU clocks temporarily to clear memory
        subprocess.run(["nvidia-smi", "-lgc", "0,0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["nvidia-smi", "-rgc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("GPU memory cleanup attempted")
        return True
    except Exception as e:
        print(f"GPU memory cleanup failed: {e}")
        return False

def trim_frames(input_path, start_time, end_time,count,foldername=None):
    if not os.path.isfile(input_path):
        print(f"Error: The file '{input_path}' does not exist.")
        return None
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(foldername, f"{file_name}-trim({start_time}-{end_time}).mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(file_dir, f"{file_name}-trim({start_time}-{end_time}).mp4")

    try:
        cmd = [

            "ffmpeg", 
            "-i", input_path, 
            "-c:v", "h264_nvenc",  
            "-vf", f'trim=start_frame={start_time.replace("f","")}:end_frame={end_time.replace("f","")},setpts=PTS-STARTPTS',      
            "-af", f'aresample=async=1',        
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd), "\n*****************************************************************************************************")
        subprocess.run(cmd, check=True)
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not on PATH.")
        return None

def trim_video_timestamps(input_path, start_time, end_time,count,foldername=None):
    startforname = start_time.replace(":","")
    endforname = end_time.replace(":","")
    if foldername:
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        # output_path = os.path.join(foldername, f"{file_name}_trimmed{count}.mp4")
        output_path = os.path.join(foldername, f"{file_name}-trim({startforname}-{endforname}).mp4")
    else:
        file_dir = os.path.dirname(input_path)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        # output_path = os.path.join(file_dir, f"{file_name}_trimmed{count}.mp4")
        output_path = os.path.join(file_dir, f"{file_name}-trim({startforname}-{endforname}).mp4")
    try:
        cmd = [
            "ffmpeg", 
            "-i", input_path, 
            "-c:v", "h264_nvenc",  
            "-ss", start_time,      
            "-to", end_time,        
            "-y",
            "-an",                   
            output_path
        ]
        print(" ".join(cmd), "\n*****************************************************************************************************")

        subprocess.run(cmd, check=True)    
        return output_path
    
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None
    except FileNotFoundError:
        print("Error: FFmpeg not found. Make sure FFmpeg is installed and in your PATH.")
        return None

def makefolder(file_path, count=1):
    # Get directory containing the file
    folder_path = os.path.dirname(file_path)
    
    # Get just the filename without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create folder name
    resized_folder_name = f"trimmed-{count}"
    
    # Create full path to new folder
    resized_folder_path = os.path.join(folder_path, resized_folder_name)
    
    # Check if folder exists and print debug info
    print(f"Checking if folder exists: {resized_folder_path}")
    print(f"Folder exists: {os.path.exists(resized_folder_path)}")
    
    # Create the folder if it doesn't exist
    if os.path.exists(resized_folder_path):
        # messagebox.showerror("ERROR", f"DELETE the folder {resized_folder_name}")
        # os.startfile(os.path.dirname(resized_folder_path))
        # return None
        return makefolder(file_path, count+1)
    else:
        os.makedirs(resized_folder_path)
        print(f"Created folder: {resized_folder_path}")
    return resized_folder_path
    
def remove_space(stringinput):
    try:
        int(stringinput[-1])
    except:
        return stringinput[:-1]
    return stringinput
def main():
    root = tk.Tk()
    root.withdraw()
    
    file_paths = filedialog.askopenfilenames(title="Select one or multiple Video File(s)", 
                                           filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")])
    if not file_paths:
        print("No file selected. Exiting...")
        return
    
    start_times = remove_space(simpledialog.askstring("Input Values", "Start time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS):")).split(".")
    
    if start_times is None:
        print("Exiting...")
        return
    # for i in range(len(start_times)):
    #     start_times[i] = format_time_input(start_times[i])

    end_times = remove_space(simpledialog.askstring("Input Values", "End time (HHMMSS or frame number): \nIF MULTIPLE: separate by period (HHMMSS.HHMMSS)::")).split(".")
    
    unitoption = custom_dialog("Unit","What is your format?", option1="HHMMSS", option2="Frames")

    if end_times is None:
        print("Exiting...")
        return
    # for i in range(len(end_times)):
    #     end_times[i] = format_time_input(end_times[i])

    root.destroy()
    if len(start_times) > 1 and len(file_paths) == 1:
        
        foldername = makefolder(file_paths[0])
    elif len(file_paths) > 1:
        foldername = makefolder(file_paths[0])
    else:
        foldername = None
    all_processing_complete = False
    output_path = None
    
    if len(end_times) == len(start_times):
        for count, _ in enumerate(start_times):
            start_time = start_times[count]
            end_time = end_times[count]
            if unitoption == 'HHMMSS':
                start_time = format_time_input(start_time)
                end_time = format_time_input(end_time)
                print("Start time:", start_time)
                print("End time:", end_time)
                for i, path in enumerate(file_paths):
                    output_path = trim_video_timestamps(path, start_time, end_time, count, foldername)    
                # Remove this line: os.startfile(os.path.dirname(output_path))
            elif unitoption == 'Frames':
                for i, path in enumerate(file_paths):
                    if i > 0:
                        # Clear GPU memory between files
                        pass
                    output_path = trim_frames(path, start_time, end_time, count, foldername)
                
        clear_gpu_memory()
        all_processing_complete = True
    else:
        messagebox.showerror("ERROR", "Must enter same # of start times as end times")
    
    # Only open the directory once all processing is complete and multiple files were selected
    if all_processing_complete and len(file_paths) > 1 and foldername and output_path:
        os.startfile(foldername)
    elif all_processing_complete and output_path:
        os.startfile(os.path.dirname(output_path))

def custom_dialog(title, message, option1="Proceed", option2="Skip"):
    result = [False]  # Using a list to store the result
    
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.grab_set()  # Make the dialog modal
    
        # Center the dialog on the screen
    dialog.update_idletasks()  # Update "requested size" from geometry manager
    
    # Calculate position x, y
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()
    
    position_x = int(screen_width/2 - dialog_width/2)
    position_y = int(screen_height/2 - dialog_height/2)
    
    # Position the window
    dialog.geometry(f"+{position_x}+{position_y}")
    
    # Create message label
    label = tk.Label(dialog, text=message, wraplength=250, pady=20)
    label.pack()
    
    # Frame for buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=10)
    
    # Yes button with custom text
    def on_op1():
        result[0] = option1
        dialog.destroy()
    def on_op2():
        result[0] = option2
        dialog.destroy()
        
    op1_button = tk.Button(button_frame, text=option1, width=8, command=on_op1)
    op1_button.pack(side=tk.LEFT, padx=10)
    
    # No button with custom text
    op2_button = tk.Button(button_frame, text=option2, width=8, command=on_op2)
    op2_button.pack(side=tk.LEFT, padx=10)
    
    # Wait for the dialog to be closed
    dialog.wait_window()
    
    return result[0]

if __name__ == "__main__":
    main()
