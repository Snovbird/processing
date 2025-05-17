#add to comma separated string
import tkinter as tk
from tkinter import simpledialog, filedialog
import pyperclip

def main():
    setofcss = simpledialog.askstring("comma input", "Integers separated by period (HHMMSS.HHMMSS. etc):").split(".")
    # toadd = simpledialog.askinteger("integer", "toadd:")

    tocopy = ""
    temp = ""
    for css in setofcss:
        if int(css[-2:]) > 59 :
            temp = str(int(css[:-2]) + 1) + str(int(css[-2:]) - 60) 
            tocopy += temp + "."
        else:
            tocopy += css + "."
        
    if tocopy[-1] == ".":
        tocopy = tocopy[0:-1]
    pyperclip.copy(tocopy)

if __name__ == "__main__":
    main()
