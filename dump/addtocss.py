#add to comma separated string
import tkinter as tk
from tkinter import simpledialog, filedialog
import pyperclip

def main():
    setofcss = simpledialog.askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):").split(".")
    toadd = simpledialog.askinteger("integer", "toadd:")
    for c in range(len(setofcss)): #add 15
        setofcss[c] = int(setofcss[c]) + toadd


    tocopy = ""
    for css in setofcss:
        tocopy += str(css)
        tocopy += "."

    if tocopy[-1] == ".":
        tocopy = tocopy[0:-1] # REMINDER: subtract 1 to last value inside ":" since starts at [0:]

    pyperclip.copy(tocopy)

if __name__ == "__main__":
    main()
