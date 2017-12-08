import os
from django.conf import settings
#from spicy.core.simplepages.defaults import SIMPLE_PAGE_MODEL

SITESKIN_SETTINGS_MODEL = getattr(
    settings, 'SITESKIN_SETTINGS_MODEL', 'siteskin.Siteskin')

ADMIN_SITESKIN = getattr(settings, 'ADMIN_SITESKIN', None)
SITESKINS_PATH = getattr(settings, 'SITESKINS_PATH', os.path.abspath('siteskins'))

# XXX deprecated loaders.py 64L
#ABSOLUTE_SITESKIN_PATH = getattr(settings, 'SITESKINS_PATH', '')
DEFAULT_SITESKIN = getattr(settings, 'DEFAULT_SITESKIN', 'current')

SPICY_SITESKIN_FILE = getattr(settings, 'SPICY_SITESKIN_FILE', 'spicy.core')

SPICY_SITESKIN_PRODUCT_KEYS = getattr(
    settings, 'SPICY_SITESKIN_PRODUCT_KEYS',
    ['spicy.light', 'spicy.business', 'spicy.media', 'spicy.ecom']
)

# deprecated
SITESKIN = getattr(settings, 'SITESKIN', 'example.com')
SITESKIN_DEBUG = getattr(settings, 'SITESKIN_DEBUG', False)
SITESKIN_DEBUG_CODE_LEN = 3
#

OBJECTS_PER_PAGE = getattr(settings, 'OBJECTS_PER_PAGE', 50)

PAGES_FROM_START = getattr(settings, 'PAGES_FROM_START', 2)
PAGES_TO_END = getattr(settings, 'PAGES_TO_END', 2)

DEBUG_ERROR_PAGES = getattr(settings, 'DEBUG_ERROR_PAGES', False)

USE_RENDER_FROM_RESPONSE_LIKE_SSI = getattr(
    settings, 'USE_RENDER_FROM_RESPONSE_LIKE_SSI', True)
DEFAULT_TEMPLATE = getattr(settings, 'DEFAULT_TEMPLATE', 'default.html')

SITEMAP_LOOKUP_MODEL = getattr(settings, 'SITEMAP_LOOKUP_MODEL', 'none')
SITEMAP_URL = getattr(settings, 'SITEMAP_URL', '')
SITEMAP_GZIP_COMPRESSION = 6  # Must be in 1-9 interval, 1 is fastest.
#MAX_MESSAGE_STRING_LENGTH = 1000

SITESKIN_INDEX_VIEW = getattr(
    settings, 'SITESKIN_INDEX_VIEW', 'spicy.core.siteskin.views.render')
SITESKIN_CACHE_BACKEND = getattr(
    settings, 'SITESKIN_CACHE_BACKEND', 'default')


AJAX_API_VERSION = getattr(settings, 'AJAX_API_VERSION', '0.1-default')
AJAX_API_STATUS_CODE_SUCCESS = 'success'
AJAX_API_STATUS_CODE_ERROR = 'error'

DEFAULT_FILTERS = [
    ('search_text', ''),
]
ENABLE_INDEXATION = getattr(settings, 'ENABLE_INDEXATION', True)

# Sanitizer settings
USE_SANITIZER = getattr(settings, 'USE_SANITIZER', False)
ALLOWED_HTML_ELEMENTS = [
    'a', 'A', 'p', 'P', 'br', 'BR', 'LI', 'li', 'ul', 'UL', 'ol', 'OL',
    'hr', 'HR', 'u', 'U', 'i', 'I', 'b', 'B', 'STRONG', 'strong', 'em', 'EM',
    'div', 'DIV', 'BLOCKQUOTE', 'blockquote', 'sub', 'SUB', 'sup', 'SUP',
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'img', 'h1', 'h2', 'h3', 'h5',
    'iframe', 'IFRAME']
ALLOWED_HTML_ATTRIBUTES = [
    'title', 'alt', 'href', 'src', 'class', 'id', 'target', 'width',
    'height', 'src', 'frameborder', 'allowfullscreen']
# iframe video embeds from youtube
ALLOWED_HTML_CLASSES = getattr(settings, 'ALLOWED_HTML_CLASSES', {})
ESCAPE_INVALID_TAGS = True

SITEMAP_THUMB_SIZE = getattr(settings, 'SITEMAP_THUMB_SIZE', (300, 300))
SITEMAP_ROOT = getattr(settings, 'SITEMAP_ROOT', settings.PROJECT_ROOT)
SITEMAP = getattr(
    settings, 'SITEMAP',
    [
    # spicy.presscenter example
    # {
    #     'model': pr_defaults.CUSTOM_DOCUMENT_MODEL,
    #     'filter': {'is_public': True, 'pub_date__lte': now},
    #     'gen': {
    #         'loc': lambda x: x.get_absolute_url(),
    #         'changefreq': 'daily',
    #         'priority':'0.8',
    #         'has_media': True
    #     },
    # },
    # {
    #     'model': SIMPLE_PAGE_MODEL,
    #     'filter': {'sites__id__exact': settings.SITE_ID},
    #     'exclude': {'url__startswith': '/test/'},
    #     'gen': {
    #         'loc': lambda x: x.get_absolute_url(),
    #         'changefreq': 'daily',
    #         'priority': '0.7'
    #     }
    # }
    ]
)

DATETIME_FORMAT = getattr(settings, 'DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S+03:00')
OBJECTS_LIMIT = getattr(settings, 'OBJECTS_LIMIT', 20000)
