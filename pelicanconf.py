#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'zqlai'
SITENAME = 'QBlog'
#SITELOGO = 'images/my_site_logo.png'
#SITENAME = 'Keep simple but NOT stupid'
SITEURL = 'https://zqlai.github.io'
ABOUT_ME = 'A simple guy!'
#AVATAR = 'images/avatar.png'
PATH = 'content'
TIMEZONE = 'Asia/Shanghai'
DEFAULT_DATE = 'fs'
DEFAULT_LANG = 'en'
DATE_FORMATS = {
    'en': '%a, %d %b %Y',
}

CC_LICENSE = 'CC-BY-NC-SA'

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
SOCIAL = (('Zhihu(知乎)', 'https://www.zhihu.com/people/lai-zq/activities'),
          ('Google Scholar', 'https://scholar.google.com/citations?user=m9_qnBIAAAAJ&hl=en'),)

# github
GITHUB_USER = 'zqlai'
GITHUB_REPO_COUNT = 3
GITHUB_SKIP_FORK = 'false'
GITHUB_SHOW_USER_LINK = 'false'

# google stats
GOOGLE_ANALYTICS = 'UA-127465699-1'



# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# themes
#THEME = 'pelican-themes/pelican-elegant'
#THEME = 'simple'
#THEME = 'notmyidea'
#THEME = '/root/packages/pelican-themes.git/pelican-bootstrap3'
THEME = 'themes/pelican-themes/pelican-bootstrap3'
# choose the boostrap theme on https://bootswatch.com/
BOOTSTRAP_THEME = 'flatly'
BOOTSTRAP_NAVBAR_INVERSE = True # seems just changing the navbar color


PYGMENTS_STYLE = 'native'
#PYGMENTS_STYLE = 'monokai'

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
    'sitemap',
]

# tag_cloud
TAG_CLOUD_SORTING = 'alphabetically' #  Valid values: random, alphabetically, alphabetically-rev, size and size-rev
TAG_CLOUD_BADGE = True

# sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}

# rendering
TYPOGRIFY = True
USE_PAGER = True
DEFAULT_PAGINATION = 5

DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True

DISPLAY_TAGS_ON_SIDEBAR = True
TAG_CLOUD_MAX_ITEMS = 10
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5

DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'search', 'archives')

# ARTICLE INFO
USE_FOLDER_AS_CATEGORY = True
DISPLAY_ARTICLE_INFO_ON_INDEX = True
SHOW_ARTICLE_AUTHOR = True
SHOW_ARTICLE_CATEGORY = True
SHOW_DATE_MODIFIED =  True
DEFAULT_CATEGORY = 'misc'
## addthis
ADDTHIS_PROFILE = 'ra-5bc35adaf039c73e' #my ID on www.addthis.com

# url settings
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

# archives
ARCHIVES_SAVE_AS = 'archives.html'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%b}/index.html'

