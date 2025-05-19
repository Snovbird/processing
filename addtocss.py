#add to comma separated string
import tkinter as tk
from tkinter import simpledialog, filedialog
import pyperclip
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

def main():
    setofcss = simpledialog.askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):")
    if setofcss.endswith("."):
        setofcss = setofcss[:-1]
    
    setofcss = setofcss.split(".")
    
    toadd = simpledialog.askinteger("integer", "toadd:")

    for c in range(len(setofcss)):
        setofcss[c] = int(setofcss[c]) + toadd
        print(f"After adding {toadd} to value {c}: {setofcss[c]}")
    
    # Join with periods
    tocopy = ".".join(str(css) for css in setofcss)
    print(f"Before formatright: {tocopy}")
    
    formatted = formatright(tocopy)
    print(f"After formatright: {formatted}")
    
    # Copy based on choice
    choice = custom_dialog("HMMSS or FRAMES", "HMMSS or FRAMES", "HHMMSS", "FRAME")
    if choice == "FRAME":
        pyperclip.copy(tocopy)
    elif choice == "HHMMSS":
        pyperclip.copy(formatted)

def formatright(setofcss):
    time_values = setofcss.split(".")
    
    corrected_values = []
    for c, time_str in enumerate(time_values):
        print(f"\nProcessing value {c}: '{time_str}'")
        
        if len(time_str) >= 2:
            if len(time_str) == 2:
                minutes = 0
                seconds = int(time_str)
            else:
                minutes = int(time_str[:-2])
                seconds = int(time_str[-2:])
            
            print(f"  Initial parse: minutes={minutes}, seconds={seconds}")
            
            # Fix values where seconds exceed 59
            if seconds > 59:
                additional_mins = seconds // 60
                seconds = seconds % 60
                minutes += additional_mins
                print(f"  Adjusting: +{additional_mins} min, now minutes={minutes}, seconds={seconds}")
            
            # Format back to MMSS format
            corrected = f"{minutes:02d}{seconds:02d}"
            corrected_values.append(corrected)
            print(f"  Final formatted value: {corrected}")
    
    return ".".join(corrected_values)

if __name__ == "__main__":
    main()
