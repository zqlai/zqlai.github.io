#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'zqlai'
SITENAME = 'Keep simple but NOT stupid'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Hongkong'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# themes
#THEME = 'pelican-themes/pelican-elegant'
#THEME = 'simple'
#THEME = 'notmyidea'
#THEME = '/root/packages/pelican-themes.git/pelican-bootstrap3'
THEME = 'themes/pelican-themes/pelican-bootstrap3'

# for pelican-bootstrap3 theme
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
