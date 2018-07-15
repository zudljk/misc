from subprocess import Popen
from sys import stdin
from os import stat

for path in stdin.readlines():
    stat()
    wrapAsMP4(path)

def wrapAsMP4(mtsfile):
    proc = Popen(["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy", "-f", "mp4", ])