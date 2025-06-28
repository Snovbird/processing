import pyperclip
from common.common import askstring,askint
a = askint(msg="Enter Start start time:",title="Start time")
d = [a]
e = 1
for i in range(10):
    for b in [40,80,150]:
        a+= b + 40
        d.append(a)
del d[-1]

dsplus = None
dsplus = True

Cycle = "DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS+.DS+.DS-.DS+.DS-.DS-.DS+.DS-.DS+.DS-.DS-.DS+.DS+.DS-.DS+.DS-.DS+.DS-.DS+.DS-.DS-.DS+".split(".")

Cycle = askstring(msg="Enter Period-Separated DS values: ",title="DS Order").split(".")
if not Cycle:
    pass
print(len([i for i in Cycle if i == "DS+"]),"DS+")
print(len([i for i in Cycle if i == "DS-"]),"DS-")
dspluslist = [d[i] for i, ds in enumerate(Cycle) if ds == "DS+"]
dsminuslist = [d[i] for i, ds in enumerate(Cycle) if ds == "DS-"]

if dsplus is True:
    
    pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dspluslist)])) # if number % 2 == 0

if not dsplus:
    
    pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(dsminuslist)])) # if number % 2 != 0

