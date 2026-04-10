import os

a = {"a":[1,2,3]}

for v in a.values():
    a = [i+2 for i in v]
    v.clear()
    v.extend(a)
    
print(a)
