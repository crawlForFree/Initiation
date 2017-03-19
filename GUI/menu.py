import tkinter as tk
from tkinter import *
import os, signal
import sys
from multiprocessing import *
from threading import Thread


def crow():
    ruin = "python3 gui.py"
    t = Thread(target= lambda: os.system(ruin))
    t.start()



def detector():
    pass

def filler():
    pass

def killMe():
    id = os.getpid()
    os.kill(id, signal.SIGKILL)


win = tk.Tk()
win.title("CRAWLER 1.0")
win.resizable(0,0)  # It is not resizble now
win.geometry("450x250+0+0")

aLabel = Label(win, text="Web Crawler 1.0 Main Unit",fg="red")
aLabel.pack()
crawl = Button(win, text =      "                        CRAWLER APPLET                              ", command = crow, fg = "blue").place(x = 30,y=20)

formDetect = Button(win, text = "                        FORM CLLASIFICATION APPLET           ", command = detector, fg = "blue").place(x=30, y=60)

formFILL = Button(win, text =   "                        FORM FILLING APPLET                        ", command = filler, fg = "blue").place(x=30, y=100)

render = Button(win, text = "EXIT", command = killMe, fg = "red").place(x=328,y=140)


win.mainloop()
