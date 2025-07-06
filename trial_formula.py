
from common.common import askstring,askint,custom_dialog,findval,assignval

def trial_formula(start_time:int = None, first_plus_or_minus:str = None,copy_which:str="DS+",) -> str:
    if not start_time:
        start_time = askint(msg="Enter Start start time:",title="Start time")
        if not start_time:
            return
    list_of_timestamps = [start_time]

    for i in range(10):
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

    if not first_plus_or_minus:
        first_plus_or_minus = custom_dialog(msg="Which is first cue?",title="First trial",op1="DS+",op2="DS-")
        if not first_plus_or_minus:
            return
    if first_plus_or_minus == "DS+":
        Cycle = "DS+.DS-.DS+.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+".split(".")

    elif first_plus_or_minus == "DS-": # "DS-":
        Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS-.DS-.DS+".split(".")# Cycle = askstring(msg="Enter Period-Separated DS values: ",title="DS Order").split(".")
    if not Cycle:
        pass
    print(len([i for i in Cycle if i == "DS+"]),"DS+ len")
    print(len([i for i in Cycle if i == "DS-"]),"DS- len")
    dspluslist = [list_of_timestamps[i] for i, ds in enumerate(Cycle) if ds == "DS+"]
    dsminuslist = [list_of_timestamps[i] for i, ds in enumerate(Cycle) if ds == "DS-"]

    if copy_which == "DS+":

        return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dspluslist)]) # if number % 2 == 0 # Used for predictable trials

    elif copy_which == "DS-":
        
        return ".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dsminuslist)]) # if number % 2 != 0

def main():
    import pyperclip
    pyperclip.copy(trial_formula())

if __name__ == "__main__":
    main()

