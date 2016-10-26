#!/usr/bin/python
#coding: utf8

from feedgen.feed import FeedGenerator
from xml.sax.saxutils import escape
import sys
import os
import urllib

dir = sys.argv[2]
url = sys.argv[1]
feedfile = "watchlater.xml"

fg = FeedGenerator()
fg.load_extension('podcast')
fg.podcast.itunes_category('Technology','Podcasting')
fg.id(url+"watchlater")
fg.title(u"Feed für YouTube - Später Ansehen")
fg.description(u"Alle Videos aus der Playlist -Später ansehen- von YouTube")
fg.author(name='zudljk', email="zudljk@email.de")
fg.link(href=url+"watchlater.xml", rel="self")

for top, dirs, files in os.walk(dir):
    for file in files:
        p = urllib.quote(os.path.basename(top))
        f = urllib.quote(file)
        s = file.replace('’',"'").decode('utf8')
        size = os.stat(os.path.join(top, file)).st_size
        if not s == "ARCHIVE" and not s == "watchlater.xml":
                fe = fg.add_entry()
                fe.title(s)
                fe.id(url+p+"/"+f)
                fe.link(href=url+p+"/"+f, rel="self")
                fe.enclosure(url+p+"/"+f, str(size), 'video/mp4')
                fg.rss_str()

print fg.rss_str(pretty=True)
fg.rss_file(os.path.join(dir,feedfile))
