#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import stat
import sys
import getopt
import datetime
import hashlib

def usage():
    print("Usage:")
    print(sys.argv[0]+" [options] dir...")
    print("""Find duplicate files

Options:
-h, --help\tShow help
-t, --ignore-mtime\tIgnore mtime when comparing files
""")

def handle(exception, item):
    sys.stderr.write("Error {}: {}: {}\n".format(exception.errno, exception.strerror, item))

def hash(file):
    try:
        hash = hashlib.md5()
        with open(file, 'rb') as f:
            data = f.read(655360)
            while data:
                hash.update(data)
                data = f.read(65536)
        return hash.hexdigest()
    except Exception as e:
        handle(e, file)

def mtime(file):
    return os.stat(file).st_mtime
    
def filesize(file):
    if stat.S_ISLNK(os.lstat(file).st_mode):
        return 0
    return os.path.getsize(file)

def push(map, key, value):
    if not key:
        return
    if key in map:
        map[key].append(value)
    else:
        map[key] = [value]

def filePot(roots):
    filesInspected = 0
    for root in roots:
        for top, dirs, files in os.walk(root):
            for file in files:
                filesInspected += 1
                sys.stderr.write("Files inspected: {}     \r".format(filesInspected))
                sys.stderr.flush()    
                yield os.path.join(top, file)

def duplicatesFound(pot, destMap, methods):
    map = {}
    found = False
    # partition the pot into smaller pots according to the submitted method
    for item in pot:
        try:
            push(map, methods[0](item), item)
        except OSError as e:
            handle(e, item)
    # iterate over all the smaller pots and partition them recursively
    if len(methods) > 1:
        while map:
            key, subpot = map.popitem()
            if len(subpot) > 1:
                found = duplicatesFound(subpot, destMap, methods[1:]) or found
    # no further recursion: print out all found files with equal criterion according to methods[-1]
    else:
        for fp, files in map.iteritems():
            if len(files) > 1:
                for file in files:
                    found = True
                    s = os.stat(file)
                    print("{}\t{}k\t{}\t{}".format(file, s.st_size / 1024, str(datetime.datetime.fromtimestamp(s.st_mtime)), fp))
    return found

fpmethod = [filesize,mtime,hash]

try:
    opts, roots = getopt.getopt(sys.argv[1:],"t",["ignore-mtime"])
except getopt.GetoptError:
    usage()
    sys.exit(1)
    
for opt, arg in opts:
    if opt in ("-t", "--ignore-mtime"):
        del fpmethod[1]
    else:
        usage()
        sys.exit()

if len(roots) == 0:
    roots = ["."]

if not duplicatesFound(filePot(roots), {}, fpmethod):
    sys.stderr.write("No duplicates found.\n")
