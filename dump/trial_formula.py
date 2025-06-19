import pyperclip
a = 25
d = [25]
for i in range(10):
    for b in [40,80,150]:
        a += (b+40)
        d.append(a)
pyperclip.copy(".".join([f'{ a//60}{str(a % 60).zfill(2)}' for a in d]))