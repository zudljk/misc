#!/usr/bin/python
#coding: utf8

from feedgen.feed import FeedGenerator
from xml.sax.saxutils import escape
import sys
import os
import urllib
import pytz
from datetime import datetime

url = sys.argv[1]
dir = os.path.dirname(sys.argv[2])
feedfile = os.path.basename(sys.argv[2])

fg = FeedGenerator()
fg.load_extension('podcast')
fg.podcast.itunes_category('Technology','Podcasting')
fg.podcast.itunes_author('zudljk@email.de')
fg.podcast.itunes_owner(name='zudljk', email='zudljk@email.de')
fg.id(url+"/"+feedfile)
fg.title(u"Feed für YouTube - Später Ansehen")
fg.description(u"Alle Videos aus der Playlist -Später ansehen- von YouTube")
fg.author(name='zudljk', email="zudljk@email.de")
fg.link(href=url+"/"+feedfile, rel="self")

for top, dirs, files in os.walk(dir):
    for file in files:
        fp = os.path.join(top, file)
        p = urllib.quote(os.path.basename(top))
        f = urllib.quote(file)
        s, format = os.path.splitext(file)
        s = s.replace('’',"'").decode('utf8')
        t = pytz.utc.localize(datetime.fromtimestamp(os.path.getctime(fp)))
        size = os.stat(fp).st_size
        if not s == "ARCHIVE" and not file == feedfile:
                fe = fg.add_entry()
                fe.title(s)
                fe.description(s)
                fe.guid(url+p+"/"+f, )
                fe.published(t)
                fe.enclosure(url+p+"/"+f, str(size), 'video'+format.replace(".","/"))
                fg.rss_str()

print fg.rss_str(pretty=True)
fg.rss_file(os.path.join(dir,feedfile))
