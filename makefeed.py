#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
        fe = fg.add_entry()
        fe.id(url+urllib.quote_plus(file))
        fe.title(escape(os.path.basename(file)))
        fe.link(href=url+urllib.quote_plus(file), rel="self")

fg.rss_file(os.path.join(dir,feedfile))
