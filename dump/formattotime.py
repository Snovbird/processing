import tkinter as tk
from tkinter import simpledialog
import pyperclip

def main():
    # Get input string from dialog or use example
    # Uncomment next line to get user input
    # setofcss = simpledialog.askstring("Time Format", "Enter comma-separated time values:")
    setofcss = simpledialog.askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):")
    try:
        int(setofcss)[-1]
    except :
        setofcss = setofcss[:-1]
    setofcss = setofcss.split(".")
    # Split the string by periods 645.845.1314.2454.2813.3124.3444
    corrected_values = []
    for c,time_str in enumerate(setofcss):
        if len(time_str) >= 2:  # Make sure it has at least 2 digits
            # Extract minutes and seconds
            if len(time_str) == 2:
                minutes = 0
                seconds = int(time_str)
                print(f"time REFORMATTED {c}:",f"{minutes:02d}{seconds:02d}")
            else:
                minutes = int(time_str[:-2])
                seconds = int(time_str[-2:])
                
            # Fix values where seconds exceed 59
            if seconds > 59:
                minutes += seconds // 60
                seconds = seconds % 60
            
            # Format back to MMSS format
            corrected = f"{minutes:02d}{seconds:02d}"
            corrected_values.append(corrected)
    
    # Join the corrected values with periods
    tocopy = '.'.join(corrected_values)
    pyperclip.copy(tocopy)
    print(f"copied: {tocopy}")

if __name__ == "__main__":
    main()



