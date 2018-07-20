from os import path, walk, stat, mkdir, remove, utime
from subprocess import Popen, PIPE
from string import upper
from time import localtime
from pwd import getpwuid
import logging


def wrap_as_mp4(mts_file, metadata, output_dir=None):
    if output_dir is None:
        output_dir = path.dirname(mts_file)

    if not path.isdir(output_dir):
        mkdir(output_dir)

    mp4file, mts = path.splitext(mts_file)
    mp4file = path.join(output_dir, path.basename(mp4file)) + '.mp4'

    params = ["/usr/local/bin/ffmpeg",
              "-i", mts_file,
              "-vcodec", "copy",
              "-acodec", "copy",
              "-n",
              "-nostats",
              "-loglevel", "error"
              ]
    for key, value in metadata.iteritems():
        params.append("-metadata")
        params.append(key + '=' + str(value))
    params.append(mp4file)

    try:
        so, se = Popen(args=params, stderr=PIPE).communicate()
        if len(se) > 0:
            raise RuntimeError(se)
        s = stat(mts_file)
        utime(mp4file, (s.st_atime, s.st_mtime))
    except Exception as e:
        raise RuntimeError('Call to ffmpeg failed: %s' % str(e))


def get_user_full_name(uid):
    return getpwuid(uid).pw_gecos


def wrap_avchd_dir(avchd_dir):
    user = get_user_full_name(stat(avchd_dir).st_uid)
    outdir = path.join(path.dirname(avchd_dir), "mp4")
    title = path.basename(path.dirname(avchd_dir))
    for top, dirs, files in walk(path.join(avchd_dir, "BDMV", "STREAM")):
        for g in files:
            wrap_mts_file(path.join(top, g), outdir, user, title)


def wrap_mts_file(mts_file, outputdir=None, user=None, title=None):
    if user is None:
        user = get_user_full_name(stat(mts_file).st_uid)
    if title is None:
        title = path.basename(path.dirname(mts_file))
    if not path.exists(mts_file):
        raise OSError('%s not found' % mts_file)
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
            "track": track + 1
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
        logger.error(str(e))
        raise e
