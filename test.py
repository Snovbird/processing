
# string = "00018.00338.00648.01008.01438.02108.02618.02738.03248.03608.03918.04548.04908.05338.10008.10208"



# print(len(string.split(".")))

from common.common import findval,askint

fill = findval("batch_size")
print(fill)
batch_size:int = askint(msg="How many clips at once?",title="Batch size",fill=7)
print(batch_size)

