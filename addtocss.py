#add to comma separated string
from common.common import askstring,askint
import pyperclip

from common.common import custom_dialog


def main():
    setofcss = askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):")
    if setofcss.endswith("."):
        setofcss = setofcss[:-1]
    
    setofcss = setofcss.split(".")
    
    toadd = askint("integer", "toadd:")

    for c in range(len(setofcss)):
        setofcss[c] = int(setofcss[c]) + toadd
        print(f"After adding {toadd} to value {c}: {setofcss[c]}")
    
    # Join with periods
    tocopy = ".".join(str(css) for css in setofcss)
    print(f"Before formatright: {tocopy}")
    
    formatted = formatright(tocopy)
    print(f"After formatright: {formatted}")
    # Copy based on choice 
    choice = custom_dialog(title="HMMSS or FRAMES", msg="HMMSS or FRAMES", op1="HHMMSS", op2="FRAME")
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
