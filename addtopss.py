#add to comma separated string
from common.common import askstring, askint, custom_dialog,hhmmss_to_seconds,seconds_to_hhmmss,error


def addtopss(time_input:list[str]|str,toadd:int|None = None,HHMMSS_or_frames:str = None) -> list[str] : # add a given value to each period-separated value
    
    if not toadd:
        toadd = askint(title="Enter integer", msg="Number of SECONDS to add:")
    if not toadd:
        return

    # Copy based on choice
    if not HHMMSS_or_frames:
        HHMMSS_or_frames = custom_dialog(title="HHMMSS or FRAMES", msg="HHMMSS or FRAMES", op1="HHMMSS", op2="FRAME")

    # **************************************            FRAMES          **************************************
    if HHMMSS_or_frames == "FRAME":
        try:
            time_input = [int(i) for i in time_input]
        except:
            error("Addtopss input cannot be formatted as integers")
            return
        for c, value in enumerate(time_input):
            time_input[c] += toadd
            # Join with periods
            tocopy = [str(i) for i in list_of_values]
        return tocopy
    
    # **************************************            HHMMSS          **************************************
    elif HHMMSS_or_frames == "HHMMSS":

        # Handling weird/missing inputs: can accept period-separated strings; preferable input = list[str]
        if type(time_input) == str and "." in time_input:
            list_of_values = [hhmmss_to_seconds(i) for i in time_input.split(".")]
        elif type(time_input) == str and "." not in time_input:
            list_of_values = [hhmmss_to_seconds(time_input)]
        else: # preferable list input
            list_of_values = [hhmmss_to_seconds(str(numberstring)) for numberstring in time_input.copy()] # LISTS ARE MUTABLE


        for c, value in enumerate(list_of_values):
            list_of_values[c] += toadd
            # Join with periods
            # tocopy = [str(i) for i in list_of_values]

        
        formatted = [seconds_to_hhmmss(number) for number in list_of_values.copy()]

        return formatted



if __name__ == "__main__":
    setofpss = askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):").split(".")
    import pyperclip
    pyperclip.copy(".".join(addtopss(setofpss)))
    
        # def formatright(time_values):
        #     corrected_values = []
        #     for c, time_str in enumerate(time_values.split(".")):
        #         print(f"\nProcessing value {c}: '{time_str}'")
                
        #         # Initialize hours, minutes, and seconds
        #         hours = 0
        #         minutes = 0
        #         seconds = 0
                
        #         # Parse based on string length
        #         str_len = len(time_str)
        #         if str_len == 2:  # SS format
        #             seconds = int(time_str)
        #         elif str_len == 4:  # MMSS format
        #             minutes = int(time_str[:-2])
        #             seconds = int(time_str[-2:])
        #         elif str_len in [5,6]:  # HHMMSS format
        #             hours = int(time_str[:-4])
        #             minutes = int(time_str[-4:-2])
        #             seconds = int(time_str[-2:])
        #         else:  # Handle any other length by converting all to seconds first
        #             total_seconds = int(time_str)
        #             hours = total_seconds // 3600
        #             minutes = (total_seconds % 3600) // 60
        #             seconds = total_seconds % 60
                
        #         # print(f"  Initial parse: hours={hours}, minutes={minutes}, seconds={seconds}")
                
        #         # Fix values where seconds exceed 59
        #         if seconds >= 60:
        #             additional_mins = seconds // 60
        #             seconds = seconds % 60
        #             minutes += additional_mins
        #             # print(f"  Adjusting seconds: +{additional_mins} min, now minutes={minutes}, seconds={seconds}")
                
        #         # Fix values where minutes exceed 59
        #         if minutes >= 60:
        #             additional_hours = minutes // 60
        #             minutes = minutes % 60
        #             hours += additional_hours
        #             # print(f"  Adjusting minutes: +{additional_hours} hr, now hours={hours}, minutes={minutes}")
                
        #         # Format back to HHMMSS format
        #         corrected = f"{hours:02d}{minutes:02d}{seconds:02d}"
        #         corrected_values.append(corrected)
        #         # print(f"  Final formatted value: {corrected}")
            
        #     # return ".".join(corrected_values)
        #     return corrected_values
