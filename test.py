
# string = "00018.00338.00648.01008.01438.02108.02618.02738.03248.03608.03918.04548.04908.05338.10008.10208"



# print(len(string.split(".")))

from common.common import group_from_end


start_times = [i for i in range(16)]
print(start_times)
start_times_list = group_from_end(start_times, 7)
print(start_times_list)