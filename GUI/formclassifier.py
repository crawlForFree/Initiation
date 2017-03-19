import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os, signal
import sys
from multiprocessing import *
from threading import Thread

win = tk.Tk()
win.title("CRAWLER 1.0")
win.resizable(0,0)  # It is not resizble now
win.geometry("450x250+510+0")



def run():
    dlg = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                           filetypes=[("Text Files", "*.txt")])
    test = StringVar()
    test = dlg
    denis.set(test)
    print(denis.get())


def startme():
    ruin = "python3 " + "/home/pritish/PycharmProjects/untitled/form_classifier.py " + denis.get()
    t = Thread(target=lambda: os.system(ruin))
    t.start()

def cold():
    ruin = os.getpid()
    os.kill(ruin, signal.SIGKILL)

aLabel = Label(win, text="Web Crawler 1.0 : Unit 2.0",fg="red")
aLabel.pack()

denis = StringVar()

enterhere = Label(win, text = "Enter file address here : ").place(x = 15,y = 30)

entry = Entry(win, textvariable = denis, width = 52).place(x=15,y=50)

opening = Button(win, text = "Or Open from here", command = run, fg = "blue").place(x=157,y=80)

start = Button(win, text = "Start Classifying    ", command = startme, fg = "blue").place(x=157,y=110)

stop = Button(win, text = "Exit", command = cold, fg = "red").place(x=248, y=140)

win.mainloop()
