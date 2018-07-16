from sys import stdin
from os import path
from os import walk
from os import remove
from os import environ
from subprocess import Popen
from subprocess import PIPE
from string import upper


def wrap_as_mp4(mtsfile, metadata={}):
    mp4file, mts = path.splitext(mtsfile)
    params = ["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy", mp4file + '.mp4']
    for key, value in metadata:

    proc = Popen(params)
    so, se = proc.communicate(PIPE)
    for i in so.readlines():
        print i
    if proc.returncode == 0:
        remove(mtsfile)


def get_user_full_name():
    proc = Popen(['finger', environ["USER"]])
    sti, ste = proc.communicate(PIPE)
    for i in so.readlines():



for f in stdin.readlines():
    if path.isdir(f):
        if path.basename(f) == 'AVCHD':
            dirmetadata = {
                "title": path.basename(path.dirname(f)),
                "author": environ['USER']}
            f = path.join(f, "BDMV", "STREAM")
            for top, dirs, files in walk(f):
                for g in files:
                    b, extension = path.splitext(g)
                    if upper(extension) == '.MTS':
                        wrap_as_mp4(path.join(top, g))
    else:
        wrap_as_mp4(f)
