
from common.common import askstring,askint,custom_dialog,findval,assignval
def div(arg1,arg2):
    try:
        return arg1 / arg2
    except ZeroDivisionError:
        return 0
def trial_formula(plus_or_minus_first:str|None = None,extract_which:str|None=None):
    
    start_time = askint(msg="Enter Start start time:",title="Start time",fill=findval("start_time"))
    assignval("start_time",start_time)
    list_of_timestamps = [start_time]
    e = 1
    for i in range(10): # 10*3 = 30 times to go through
        for ITI_len in [40,80,150]:
            start_time += ITI_len + 40
            list_of_timestamps.append(start_time)
    del list_of_timestamps[-1]


    # which_first = custom_dialog(msg="Which trial goes first?",title="First trial",op1="DS+",op2="DS-")
    if False:
        session_number = askint(msg="Enter session number:",title="Session number",fill=findval("session_number"))


        assignval("session_number",session_number)

        Cycle = None
        if session_number % 2 == 0: #"DS+":
            Cycle = "DS+.DS-.DS+.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+".split(".")

        elif session_number % 2 != 0: # "DS-":
            Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS-.DS-.DS+".split(".")

    if plus_or_minus_first is None:
        plus_or_minus_first = custom_dialog(msg="Which is FIRST cue?",title="First trial",op1="DS+",op2="DS-")
        print("plus or minus = ",plus_or_minus_first)
        if not plus_or_minus_first:
            return
    if plus_or_minus_first == "DS+":
        Cycle = "DS+.DS-.DS+.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+"
    elif plus_or_minus_first == "DS-": # "DS-":
        Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS-"# Cycle = askstring(msg="Enter Period-Separated DS values: ",title="DS Order").split(".")
    if not Cycle:
        pass
    
    Cycle = Cycle.split(".")
    # Cycle = askstring(msg="Is this the right order:",title="Verification",fill=Cycle).split(".")
    if not Cycle:
        return
    print(len([i for i in Cycle if i == "DS+"]),"DS+ len")
    print(len([i for i in Cycle if i == "DS-"]),"DS- len")
    dspluslist = [list_of_timestamps[i] for i, ds in enumerate(Cycle) if ds == "DS+"]
    dsminuslist = [list_of_timestamps[i] for i, ds in enumerate(Cycle) if ds == "DS-"]
    ITIlist = [list_of_timestamps[i]+ 40*(1 if div(i% 2, i% 2) != 0 else 0) for i in range(1,len(Cycle))]
    if not extract_which:
        extract_which = custom_dialog(msg="GET VALUES FOR WHICH CUE?\n This will give timestamps for: DS+, ITI or DS-",title="First trial",op1="DS+",op2="ITI",op3="DS-") # = "DS+" # Timestamps for which of the two cue lights (plus or minus) will be copied

    if extract_which == "DS+":
        print("dsplus")
        return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dspluslist)]) # if number % 2 == 0 # Used for predictable trials
    elif extract_which == "ITI":
        ITIchoice =custom_dialog("start_times or end times","Timestamps","start","end") 
        if ITIchoice == "start":
            return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(ITIlist) if number % 2 == 0])
        elif ITIchoice == "end":
            return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(ITIlist) if number % 2 != 0])
    elif extract_which == "DS-":
        print("dsminus")
        return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dsminuslist)]) # if number % 2 != 0

def main():
    import pyperclip
    pyperclip.copy(trial_formula())

if __name__ == "__main__":
    main()

