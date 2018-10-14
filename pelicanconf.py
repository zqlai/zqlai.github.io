#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'zqlai'
SITENAME = 'Keep simple but NOT stupid'
SITEURL = ''
ABOUT_ME = 'A simple guy!'

PATH = 'content'

TIMEZONE = 'Hongkong'
DEFAULT_DATE = 'fs'

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
         )

# Social widget
SOCIAL = (('zhihu(知乎)', 'https://www.zhihu.com/people/lai-zq/activities'),
          ('Google Scholar', 'https://scholar.google.com/citations?user=m9_qnBIAAAAJ&hl=en'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# themes
#THEME = 'pelican-themes/pelican-elegant'
#THEME = 'simple'
#THEME = 'notmyidea'
#THEME = '/root/packages/pelican-themes.git/pelican-bootstrap3'
THEME = 'themes/pelican-themes/pelican-bootstrap3'
BOOTSTRAP_THEME = 'flatly'

# for pelican-bootstrap3 theme
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGIN_PATHS = ['plugins/pelican-plugins']
I18N_TEMPLATES_LANG = 'en'

# PLUGINS
PLUGINS = [
    'i18n_subsites',
    'liquid_tags.img',
    'liquid_tags.video',
    'liquid_tags.youtube',
    'liquid_tags.vimeo',
    'liquid_tags.include_code',
    'tipue_search',
    'related_posts',
    'tag_cloud',
]


# rendering
TYPOGRIFY = True
DEFAULT_PAGINATION = 5
TAG_CLOUD_MAX_ITEMS = 10
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True
DISPLAY_TAGS_ON_SIDEBAR = True
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'search', 'archives')

# ARTICLE INFO
USE_FOLDER_AS_CATEGORY = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
SHOW_ARTICLE_AUTHOR = True
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED =  True
DEFAULT_CATEGORY = 'misc'

# url settings
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# archives
ARCHIVES_SAVE_AS = 'archives.html'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%b}/index.html'

