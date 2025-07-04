import pyperclip
from common.common import askstring,askint,custom_dialog,findval,assignval

def trial_formula(plus_or_minus:str|None = None)
    a = askint(msg="Enter Start start time:",title="Start time")
    d = [a]
    e = 1
    for i in range(10):
        for b in [40,80,150]:
            a+= b + 40
            d.append(a)
    del d[-1]


    # which_first = custom_dialog(msg="Which trial goes first?",title="First trial",op1="DS+",op2="DS-")
    if False:
        session_number = askint(msg="Enter session number:",title="Session number",fill=findval("session_number"))


        assignval("session_number",session_number)

        Cycle = None
        if session_number % 2 == 0: #"DS+":
            Cycle = "DS+.DS-.DS+.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+".split(".")

        elif session_number % 2 != 0: # "DS-":
            Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS-.DS-.DS+".split(".")

    if not plus_or_minus:
        plus_or_minus = custom_dialog(msg="Which is first cue?",title="First trial",op1="DS+",op2="DS-")
    if not plus_or_minus:
        return
    if plus_or_minus == "DS+":
        Cycle = "DS+.DS-.DS+.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS+".split(".")

    elif plus_or_minus == "DS-" # "DS-":
        Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS-.DS-.DS+".split(".")# Cycle = askstring(msg="Enter Period-Separated DS values: ",title="DS Order").split(".")
    if not Cycle:
        pass
    print(len([i for i in Cycle if i == "DS+"]),"DS+")
    print(len([i for i in Cycle if i == "DS-"]),"DS-")
    dspluslist = [d[i] for i, ds in enumerate(Cycle) if ds == "DS+"]
    dsminuslist = [d[i] for i, ds in enumerate(Cycle) if ds == "DS-"]



    dsplus = None
    dsplus = True
    if dsplus is True:
        
        pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dspluslist)])) # if number % 2 == 0

    if not dsplus:
        
        pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dsminuslist)])) # if number % 2 != 0

def main():
    
    trial_formula()

if __name__ == "__main__":
    main()

