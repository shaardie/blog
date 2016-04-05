#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sven Haardiek'
SITENAME = u'blog.haardiek.org'
SITEURL = u'http://blog.haardiek.org'

EMAIL = u"sven@haardiek.de"
GITHUB_URL = "https://github.com/shaardie"
TWITTER_USERNAME = "haardiek"

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'

ARCHIVES_URL       = 'archives'
ARCHIVES_SAVE_AS   = 'archives/index.html'

MENU_INTERNAL_PAGES = (
    ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
)

SOCIAL = (('Twitter', 'https://twitter.com/haardiek'),
          ('Github', 'https://github.com/shaardie'))

THEME = 'blue-penguin'

STATIC_PATHS = ['images', 'files']

RELATIVE_URLS = True
