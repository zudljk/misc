#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from os import path
from os import listdir
from os import popen

rsyncTemplate = "echo /usr/local/bin/rsync --archive --verbose --delete-after --exclude .Doc* --exclude .fs* --exclude .Spot* --exclude .Trash* --exclude .Temp* --exclude Backup"
sourcePath = path.dirname(path.realpath(__file__))
targetPath = "/Volumes/SeagateExp/Bilder"

if sourcePath.startswith(targetPath):
    targetPath = targetPath.replace(old="SeagateExp", new="SeagateUSB3")

years = listdir(sourcePath)


class PhotoRsync(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Syncing ...")

        self.geometry('400x205')
        self.lbl = Label(self, text="Hello", anchor="nw", justify=LEFT, borderwidth=2)
        self.lbl.place(x=15, y=10)
        self.lbl.pack()
        style = Style()
        style.configure("black.Horizontal.TProgressbar", background='blue', padx=20, justify=CENTER)
        self.progressbar = Progressbar(self, length=370, mode="determinate", style="black.Horizontal.TProgressbar")
        self.progressbar.place(x=15, y=40)
        self.progressbar.pack()
        self.output = Text(self, height=8, width=80, bg="seashell3")
        self.output.pack()
        self.ok = Button(self, text="Ok", command=self.destroy, state=DISABLED)
        self.ok.place(x=180, y=60)
        self.ok.pack()

    def start(self):
        self.progressbar['value'] = 0
        self.progressbar["maximum"] = len(years)
        self.progressbar.pack()
        self.copy(years)

    def copy(self, sources):
        year = sources.pop(0)
        self.lbl["text"] = f"{sourcePath}/{year}"
        with popen(f"{rsyncTemplate} {year} {targetPath}/{year}") as f:
            line = f.readline()
            while line:
                self.output.insert(END, line)
                line = f.readline()
        self.progressbar['value'] += 1
        if len(sources) > 0:
            self.after(100, self.copy, sources)
        else:
            self.ok["state"] = NORMAL


app = PhotoRsync()
app.start()
app.mainloop()
