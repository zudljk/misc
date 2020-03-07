# misc

Miscellaneous Python scripts

## duplicates.py

Iterates recursively through the given paths and tries to find duplicate files.
Files are considered duplicate if their size, mtime and md5sum are equal.
The parameter -t will cause the program to ignore the mtime.

Python version: 3

## helloworld.py

Duh.

Python version: 2

## photorsync.py

A script to synchronize 2 external drives called SeagateUSB3 and SeagateExt.
Expects a folder named "Bilder" to exist on both volumes, containing folders named after years.
Only years after 2000 are supported.

Python version: 3

## revocate_mlp.py

A script to automatically generate letters to an insurance company (MLP) that revoke
the annual increase of the monthly premium by 1% (dynamic premium).

## avchd_rewrapper.py

A package using ffmpeg to re-wrap AVCHD files produced by a Canon HD21 camera into the MP4 container format.
Encoding of the audio and video streams is preserved.
The script consists of a macOS Automator workflow and a python package.

Python version: 2