#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from os import path
from os import listdir
from os import popen
from os import chmod
from os import system
from stat import *
from shutil import copy

storage1 = "/Volumes/SeagateUSB3/Bilder"
storage2 = "/Volumes/SeagateExp/Bilder"

rsyncTemplate = "echo /usr/local/bin/rsync --archive --verbose --delete-after --exclude .Doc* " \
                "--exclude .fs* --exclude .Spot* --exclude .Trash* --exclude .Temp* --exclude Backup"

sourcePath = path.dirname(path.realpath(__file__))
targetPath = storage2

if sourcePath.startswith(targetPath):
    targetPath = storage1
elif not sourcePath.startswith(storage1):
    copy(path.realpath(__file__), path.join(storage1, "photosync.command"))
    copy(path.realpath(__file__), path.join(storage2, "photosync.command"))
    mode = S_IXUSR + S_IRUSR + S_IWUSR + S_IRGRP + S_IXGRP + S_IROTH + S_IXOTH
    chmod(path.join(storage1, "photosync.command"), mode)
    chmod(path.join(storage2, "photosync.command"), mode)
    system(path.join(storage1, "photosync.command"))
    exit(0)

years = listdir(sourcePath)

class PhotoRsync(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Syncing ...")

        self.geometry('600x250')
        style = Style()
        style.configure("black.Horizontal.TProgressbar", background='blue', padx=20, justify=CENTER)

        self.lbl = Label(self, text="Hello", anchor="nw", justify=LEFT, borderwidth=2)
        self.progressbar = Progressbar(self, length=370, mode="determinate", style="black.Horizontal.TProgressbar")
        self.frame = Frame(self)
        self.output = Text(self.frame, height=8, width=280, bg="seashell3", wrap=NONE)
        self.vscrollb = Scrollbar(self.frame, command=self.output.yview)
        self.hscrollb = Scrollbar(self, command=self.output.xview, orient=HORIZONTAL)
        self.ok = Button(self, text="Ok", command=self.destroy, state=DISABLED, height=1, padx=10, pady=5)

        self.output['yscrollcommand'] = self.vscrollb.set
        self.output['xscrollcommand'] = self.hscrollb.set

        self.lbl.pack(side=TOP, fill=X)
        self.progressbar.pack(side=TOP, fill=X)
        self.vscrollb.pack(side=RIGHT, fill=Y)
        self.output.pack(side=TOP, fill=BOTH)
        self.frame.pack(side=TOP, fill=Y)
        self.hscrollb.pack(side=TOP, fill=X)
        self.ok.pack(side=BOTTOM)

    def start(self):
        self.progressbar['value'] = 0
        self.progressbar["maximum"] = len(years)
        self.progressbar.pack()
        self.copy(years)

    def copy(self, sources):
        year = sources.pop(0)
        source = path.join(sourcePath, year)
        target = path.join(targetPath, year)
        command = f"{rsyncTemplate} {year} {target}"
        self.lbl["text"] = f"{source}"
        self.output.insert(END, command)
        with popen(command) as f:
            line = f.readline()
            while line:
                self.output.insert(END, line)
                line = f.readline()
                self.output.see(END)
        self.output.see(END)
        self.progressbar['value'] += 1
        if len(sources) > 0:
            self.after(100, self.copy, sources)
        else:
            self.ok["state"] = NORMAL


app = PhotoRsync()
app.start()
app.mainloop()
