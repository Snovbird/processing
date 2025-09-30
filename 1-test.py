import pandas,os,wx
from common.common import *
import timeit,pyperclip

# dates = list(range(100))

# # append() - much faster
# time1 = timeit.timeit(lambda: dates.append(1001), number=100000)

# # concatenation - slower
# time2 = timeit.timeit(lambda: dates + [1001], number=100000)

# # append() is typically 10-50x faster

# print(f"append {time1=}")
# print(f"add {time2=}")

print(["20250611","20250612","20250613","20250616","20250618","20250623","20250625","20250626","20250627","20250804","20250808","20250811","20250923"][::-1])