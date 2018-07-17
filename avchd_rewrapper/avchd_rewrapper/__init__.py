from os import path, walk, environ, stat
from subprocess import Popen, PIPE
from string import upper, split, strip
from time import localtime


def wrap_as_mp4(mtsfile, metadata, outputdir=None):
    if outputdir is None:
        outputdir = path.dirname(mtsfile)

    mp4file, mts = path.splitext(mtsfile)
    mp4file = path.join(outputdir, path.basename(mp4file))+'mp4'

    params = ["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy"]
    for key, value in metadata:
        params.append("-metadata")
        params.append(key+'="'+value+'"')
    params.append(mp4file)

    proc = Popen(args=params, stdout=PIPE)
    so, se = proc.communicate()
    for line in so.split('\n'):
        print line
    for line in se.split('\n'):
        print line


def get_user_full_name(loginname):
    proc = Popen(args=['finger', '-s', loginname], stdout=PIPE)
    so, se = proc.communicate()
    fullname = loginname
    for line in so.split('\n'):
        if len(line) > 0:
            logon, fullname, rest = line.split('  ', 2)
    return strip(fullname)


def wrap_avchd_dir(avchd_dir):
    user = get_user_full_name(environ["USER"])
    outdir = path.join(path.dirname(avchd_dir), "mp4")
    for top, dirs, files in walk(path.join(avchd_dir, "BDMV", "STREAM")):
        for g in files:
            wrap_mts_file(g, outdir, user)


def wrap_mts_file(mts_file, outputdir=None, user=None):
    if user is None:
        user = get_user_full_name(environ["USER"])
    track, extension = path.splitext(path.basename(mts_file))
    if upper(extension) == '.MTS':
        try:
            track = int(track)
        except ValueError:
            pass
        wrap_as_mp4(mts_file, {
            "title": path.basename(path.dirname(mts_file)),
            "author": user,
            "year": localtime(stat(mts_file).st_mtime).tm_year,
            "track": track
        }, outputdir)


def wrap_to_mp4(file_or_dir):
    if path.isdir(file_or_dir):
        if path.basename(file_or_dir) == 'AVCHD':
            wrap_avchd_dir(file_or_dir)
    else:
        wrap_mts_file(file_or_dir)
