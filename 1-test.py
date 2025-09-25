import pandas,os,wx
from common.common import *
import timeit

dates = list(range(100))

# append() - much faster
time1 = timeit.timeit(lambda: dates.append(1001), number=100000)

# concatenation - slower
time2 = timeit.timeit(lambda: dates + [1001], number=100000)

# append() is typically 10-50x faster

print(f"append {time1=}")
print(f"add {time2=}")