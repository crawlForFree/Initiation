import tkinter as tk
from tkinter import *
import os, signal
import sys
from multiprocessing import *
from threading import Thread


def run():
    ruin = "python3 /home/pritish/PycharmProjects/untitled/start.py " + url.get() + " " + domain.get()
    t = Thread(target= lambda: os.system(ruin))
    t.start()



def cold():
    ruin = os.getpid()
    os.kill(ruin, signal.SIGKILL)

win = tk.Tk()
win.title("CRAWLER 1.0")
win.resizable(0,0)  # It is not resizble now
win.geometry("450x250+510+0")

url = StringVar()
domain = StringVar()

aLabel = Label(win, text="Web Crawler 1.0 Main Unit",fg="red")
aLabel.grid(row=0,column=2,sticky=N)

label2 = Label(win,text = "Enter URL to crawl :")
label2.grid(row=1, column=0, sticky=W)   # W: west, E: east, N: north, S:south

t1 = Entry(win,textvariable = url).grid(row=1,column=2)

label3 = Label(win,text = "Enter domain name :")
label3.grid(row=2, column=0, sticky=W)   # W: west, E: east, N: north, S:south

t2 = Entry(win,textvariable = domain).grid(row=2,column=2)

start = Button(win, text = "Start Crawling", command = run, fg = "blue").grid(row=3,column=2)

stop = Button(win, text = "Exit", command = cold, fg = "red").grid(row=4,column=2)


win.mainloop()
