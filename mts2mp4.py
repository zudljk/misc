from sys import stdin
from os import path, walk, remove, environ, stat
from subprocess import Popen, PIPE
from string import upper, split
from time import localtime


def wrap_as_mp4(mtsfile, metadata):
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


def wrap_avchd_dir(avchd_dir):
    for top, dirs, files in walk(path.join(avchd_dir, "BDMV", "STREAM")):
        for g in files:
            wrap_mts_file(g)


def wrap_mts_file(mts_file):
    track, extension = path.splitext(path.basename(mts_file))
    if upper(extension) == '.MTS':
        try:
            track = int(track)
        except ValueError:
            pass
        wrap_as_mp4(mts_file, {
            "title": path.basename(path.dirname(mts_file)),
            "author": u,
            "year": localtime(stat(mts_file).st_mtime).tm_year,
            "track": track
        })


u = get_user_full_name(environ["USER"])

for f in stdin.readlines():
    if path.isdir(f):
        if path.basename(f) == 'AVCHD':
            wrap_avchd_dir(f)
    else:
        wrap_mts_file(f)
