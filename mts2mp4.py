from sys import stdin
from os import path
from os import walk
from os import remove
from subprocess import Popen
from subprocess import PIPE
from string import upper


def wrapAsMP4(mtsfile):
    mp4file, mts = path.splitext(mtsfile)
    proc = Popen(["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy", mp4file + '.mp4'])
    so, se = proc.communicate(PIPE)
    for i in so.readlines():
        print i
    if proc.returncode == 0:
        remove(mtsfile)


for f in stdin.readlines():
    if path.isdir(f):
        if path.basename(f) == 'AVCHD':
            f = path.join(f, "BDMV", "STREAM")
            for top, dirs, files in walk(f):
                for g in files:
                    b, extension = path.splitext(g)
                    if upper(e) == '.MTS':
                        wrapAsMP4(path.join(top, g))
    else:
        wrapAsMP4(f)
