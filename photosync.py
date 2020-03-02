#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Style

class PhotoRsync(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Hello world!")
        self.geometry('400x75')
        self.lbl = Label(self, text="Hello", anchor="ne", justify=LEFT, borderwidth=2)
        self.lbl.place(x=15, y=10)
        self.lbl.pack()
        style = Style()
        style.configure("black.Horizontal.TProgressbar", background='blue', padx=20, justify=CENTER)
        self.progressbar = Progressbar(self, length=370, mode="determinate", style="black.Horizontal.TProgressbar")
        self.progressbar.place(x=15, y=40)

    def start(self):
        self.progressbar['value'] = 0
        self.progressbar["maximum"] = 40
        self.progressbar.pack()
        self.copy()

    def copy(self):
        self.progressbar['value'] += 1
        self.after(100, self.copy)

app = PhotoRsync()
app.start()
app.mainloop()
