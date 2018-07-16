from sys import stdin
from os import path, walk, remove, environ, stat
from subprocess import Popen, PIPE
from string import upper, split
from time import localtime


def wrap_as_mp4(mtsfile, metadata={}):
    mp4file, mts = path.splitext(mtsfile)
    params = ["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy"]
    for key, value in metadata:
        params.append("-metadata")
        params.append(key+'="'+value+'"')
    params.append(mp4file + '.mp4')

    proc = Popen(params)
    so, se = proc.communicate(PIPE)
    for i in so.splitlines():
        print i
    if proc.returncode == 0:
        remove(mtsfile)


def get_user_full_name(loginname):
    proc = Popen(['finger', '-s', loginname])
    sti, ste = proc.communicate(PIPE)
    fullname = loginname
    for i in sti.splitlines():
        logon, fullname, rest = split(i, None, 2)
    return fullname


for f in stdin.readlines():
    if path.isdir(f):
        if path.basename(f) == 'AVCHD':
            dirmetadata = {
                "title": path.basename(path.dirname(f)),
                "author": get_user_full_name(environ['USER']),
            }
            f = path.join(f, "BDMV", "STREAM")
            for top, dirs, files in walk(f):
                for g in files:
                    prefix, extension = path.splitext(g)
                    dirmetadata["track"] = prefix
                    dirmetadata["year"] = localtime(stat(g).st_mtime).tm_year
                    if upper(extension) == '.MTS':
                        wrap_as_mp4(path.join(top, g), dirmetadata)
    else:
        dirmetadata = {
            "title": path.basename(f),
            "author": get_user_full_name(environ['USER']),
            "year": localtime(stat(f).st_mtime).tm_year
        }
        wrap_as_mp4(f)
