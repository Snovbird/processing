import pyperclip
a = 25
d = [20]
e = 1
for i in range(10):
    for b in [40,80,150]:
        a+= b + 40
        d.append(a)
del d[-1]
print(len(d))

dsplus = None
dsplus = True
if dsplus is True:
    pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(d) if number % 2 == 0]))

if not dsplus:
    pyperclip.copy(".".join([f'{hh//3600:01d}{(hh%3600)//60:02d}{hh%60:02d}' for number, hh in enumerate(d) if number % 2 != 0]))



