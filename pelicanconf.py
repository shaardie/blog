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

AUTHORS_URL = 'authors'
AUTHORS_SAVE_AS = 'authors/index.html'

MENU_INTERNAL_PAGES = (
    ('Authors', AUTHORS_URL, AUTHORS_SAVE_AS),
)

SOCIAL = (('Twitter', 'https://twitter.com/haardiek'),
          ('Github', 'https://github.com/shaardie'))

THEME = 'blue-penguin'

STATIC_PATHS = ['images', 'files']
EXTRA_PATH_METADATA = {
    'files/favicon.ico': {'path': 'favicon.ico'}
}

RELATIVE_URLS = True

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["render_math"]
