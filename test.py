from common.common import format_time_colons
a = ["10000","50","7302"]
for c,i in enumerate(a):
    a[c] = format_time_colons(i)

print(a)