from common.common import dropdown,msgbox
import os
start_time = 20
list_of_timestamps = [start_time]
def div(arg1,arg2):
    try:
        return arg1 / arg2
    except ZeroDivisionError:
        return 0

for i in range(10): # 10*3 = 30 times to go through
    for ITI_len in [40,80,150]:
        start_time += ITI_len + 40
        list_of_timestamps.append(start_time)
del list_of_timestamps[-1]
print(list_of_timestamps)
Cycle = [i for i in range(30)]
ITIlist = [int(list_of_timestamps[i]+ 40*(1 if div(i% 2, i% 2) != 0 else -0.25)) for i in range(1,len(Cycle)-1)]
print(ITIlist)

ITI_start = [i for c,i in enumerate(ITIlist) if c % 2 == 0]
ITI_end = [i for c, i in enumerate(ITIlist) if c % 2 != 0]
print(f"{ITI_start=}\t{len(ITI_start)}")
print(f"{ITI_end=}\t{len(ITI_end)}")

