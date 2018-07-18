from os import path, walk, environ, stat, mkdir, remove
from subprocess import Popen, PIPE
from string import upper, strip
from time import localtime
import logging

def wrap_as_mp4(mtsfile, metadata, outputdir=None):
    if outputdir is None:
        outputdir = path.dirname(mtsfile)

    try:
        if not path.isdir(outputdir):
            mkdir(outputdir)
    except OSError:
        raise RuntimeError('Error creating %s' % outputdir)

    mp4file, mts = path.splitext(mtsfile)
    mp4file = path.join(outputdir, path.basename(mp4file))+'.mp4'

    params = ["ffmpeg", "-i", mtsfile, "-vcodec", "copy", "-acodec", "copy", "-n", "-nostats", "-loglevel", "error"]
    for key, value in metadata.iteritems():
        params.append("-metadata")
        params.append(key+'='+str(value))
    params.append(mp4file)

    proc = Popen(args=params, stderr=PIPE)
    so, se = proc.communicate()
    if len(se) > 0:
        raise RuntimeError(se)


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
    title = path.basename(path.dirname(avchd_dir))
    for top, dirs, files in walk(path.join(avchd_dir, "BDMV", "STREAM")):
        for g in files:
            wrap_mts_file(path.join(top, g), outdir, user, title)


def wrap_mts_file(mts_file, outputdir=None, user=None, title=None):
    if user is None:
        user = get_user_full_name(environ["USER"])
    if title is None:
        title = path.basename(path.dirname(mts_file))
    if not path.exists(mts_file):
        raise OSError('{} not found'.format(mts_file))
    track, extension = path.splitext(path.basename(mts_file))
    if upper(extension) == '.MTS':
        try:
            track = int(track)
        except ValueError:
            pass
        wrap_as_mp4(mts_file, {
            "title": title,
            "author": user,
            "artist": user,
            "year": localtime(stat(mts_file).st_mtime).tm_year,
            "date": localtime(stat(mts_file).st_mtime).tm_year,
            "track": track+1
        }, outputdir)
    else:
        raise RuntimeError('%s is not an MTS file' % mts_file)


def wrap_to_mp4(file_or_dir):

    logger = logging.getLogger('avchd_rewrapper')
    logfilename = path.join(path.dirname(file_or_dir), 'avchd_rewrapper.log')
    logfile = logging.FileHandler(logfilename)
    logger.addHandler(logfile)

    try:
        if path.isdir(file_or_dir):
            if path.basename(file_or_dir) == 'AVCHD':
                wrap_avchd_dir(file_or_dir)
            else:
                raise RuntimeError('%s is not an AVCHD dir' % file_or_dir)
        else:
            wrap_mts_file(file_or_dir)
        if path.getsize(logfilename) == 0:
            remove(logfilename)
    except Exception as e:
        logger.error(e.message)
        raise e
