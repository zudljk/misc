#!/usr/bin/python

import sys
from avchd_rewrapper import wrap_to_mp4

try:
    n = 0

    for f in sys.stdin:
        n += 1
        wrap_to_mp4(f.strip())

    assert n > 0, 'No files given'

    print '%d file(s) rewrapped' % n

except Exception as e:
    print e.message
