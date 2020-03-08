#!/usr/local/bin/python3
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from os import path, linesep
from glob import glob
from os import popen
from os import chmod
from os import system
from os import chdir
from stat import *
from shutil import copy
from queue import *
from threading import Thread

storage1 = "/Volumes/SeagateUSB3/Bilder"
storage2 = "/Volumes/SeagateExp/Bilder"

rsyncTemplate = "/usr/local/bin/rsync --archive --itemize-changes --verbose --delete-after --exclude .Doc* " \
                "--exclude .fs* --exclude .Spot* --exclude .Trash* --exclude .Temp* --exclude Backup"

sourcePath = path.dirname(path.realpath(__file__))
scriptName = path.basename(path.realpath(__file__))
targetPath = storage2

if sourcePath.startswith(targetPath):
    targetPath = storage1
elif not sourcePath.startswith(storage1):
    copy(path.realpath(__file__), path.join(storage1, scriptName))
    copy(path.realpath(__file__), path.join(storage2, scriptName))
    mode = S_IXUSR + S_IRUSR + S_IWUSR + S_IRGRP + S_IXGRP + S_IROTH + S_IXOTH
    chmod(path.join(storage1, scriptName), mode)
    chmod(path.join(storage2, scriptName), mode)
    system(path.join(storage1, scriptName))
    exit(0)

chdir(sourcePath)
years = sorted(glob("20*"))


class GUI:

    def __init__(self, tk, queue, endCommand):
        self.queue = queue
        self.tk = tk
        self.tk.title("Syncing ...")

        self.tk.geometry('600x250')
        style = Style()
        style.configure("black.Horizontal.TProgressbar", background='blue', padx=20, justify=CENTER)

        self.tk.lbl = Label(self.tk, text="Waiting for files", anchor="nw", justify=LEFT, borderwidth=2)
        self.tk.progressbar = Progressbar(self.tk, length=370, mode="determinate",
                                          style="black.Horizontal.TProgressbar")
        self.tk.progressbar['value'] = 0
        self.tk.progressbar["maximum"] = len(years)
        self.tk.frame = Frame(self.tk)
        self.tk.output = Text(self.tk.frame, height=8, width=280, bg="seashell3", wrap=NONE)
        self.tk.vscrollb = Scrollbar(self.tk.frame, command=self.tk.output.yview)
        self.tk.hscrollb = Scrollbar(self.tk, command=self.tk.output.xview, orient=HORIZONTAL)
        self.tk.ok = Button(self.tk, text="Ok", command=endCommand, state=DISABLED, height=1, padx=10, pady=5)

        self.tk.output['yscrollcommand'] = self.tk.vscrollb.set
        self.tk.output['xscrollcommand'] = self.tk.hscrollb.set

        self.tk.lbl.pack(side=TOP, fill=X)
        self.tk.progressbar.pack(side=TOP, fill=X)
        self.tk.vscrollb.pack(side=RIGHT, fill=Y)
        self.tk.output.pack(side=TOP, fill=BOTH)
        self.tk.frame.pack(side=TOP, fill=Y)
        self.tk.hscrollb.pack(side=TOP, fill=X)
        self.tk.ok.pack(side=BOTTOM)

    def process_incoming(self):
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                key = msg["key"]
                value = msg["value"]
                if key == "SRC":
                    self.tk.lbl["text"] = value
                    self.tk.progressbar['value'] += 1
                elif key == "END":
                    self.tk.ok["state"] = NORMAL
                else:
                    self.tk.output.insert(END, value)
                    self.tk.output.see(END)
            except Empty:
                pass


class RsyncThread:
    """
     Launch the main part of the GUI and the worker thread. periodicCall and
     endApplication could reside in the GUI part, but putting them here
     means that you have all the thread controls in a single place.
     See also: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html
     """

    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master
        # Create the queue
        self.queue = Queue()
        # Set up the GUI part
        self.gui = GUI(master, self.queue, self.end_application)
        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 0
        self.thread1 = Thread(target=self.worker_thread1)

    def start(self):
        self.running = 1
        self.thread1.start()
        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodic_call()

    def periodic_call(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.process_incoming()
        if self.running:
            self.master.after(200, self.periodic_call)
        else:
            self.master.destroy()

    def worker_thread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while len(years) > 0:
            year = years.pop(0)
            source = path.join(sourcePath, year)
            target = path.join(targetPath, year)
            self.queue.put({"key": "SRC", "value": source})

            command = f"{rsyncTemplate} {year} {target}"
            self.queue.put({"key": "CMD", "value": command+linesep})
            with popen(command) as f:
                line = f.readline()
                while line:
                    self.queue.put({"key": "OUT", "value": line})
                    line = f.readline()
        self.queue.put({"key": "END", "value": None})

    def end_application(self):
        self.running = 0


root = Tk()
RsyncThread(root).start()
root.mainloop()
