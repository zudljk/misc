from sys import stdin
from avchd_rewrapper import wrap_to_mp4
import logging

logging.getLogger('root').addHandler(logging.FileHandler('avchd_rewrapper.log'))

wrap_to_mp4('/Volumes/Macintosh-HD/Users/oliver/Desktop/20111029/AVCHD')