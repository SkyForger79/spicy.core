import os
from django.conf import settings


SITESKIN_SETTINGS_MODEL = getattr(settings, 'SITESKIN_SETTINGS_MODEL', 'siteskin.Siteskin')


ADMIN_THEME = getattr(settings, 'ADMIN_THEME', None)
DEFAULT_THEME = getattr(settings, 'DEFAULT_THEME', 'current')
THEMES_PATH = getattr(settings, 'THEMES_PATH', os.path.abspath('../siteskins'))
SPICY_THEME_FILE = getattr(settings, 'SPICY_THEME_FILE', 'spicy.theme')

SPICY_THEME_PRODUCT_KEYS = getattr(
    settings, 'SPICY_THEME_PRODUCT_KEYS', 
    ['spicy.light', 'spicy.business', 'spicy.media', 'spicy.ecom']
    )

# deprecated
SITESKIN = getattr(settings, 'SITESKIN', 'example.com')
SITESKIN_DEBUG = getattr(settings, 'SITESKIN_DEBUG', settings.DEBUG)
SITESKIN_DEBUG_CODE_LEN = 3
#

OBJECTS_PER_PAGE = getattr(settings, 'OBJECTS_PER_PAGE', 50)

PAGES_FROM_START = getattr(settings, 'PAGES_FROM_START', 2)
PAGES_TO_END = getattr(settings, 'PAGES_TO_END', 2)

DEBUG_ERROR_PAGES = getattr(settings, 'DEBUG_ERROR_PAGES', False)

USE_RENDER_FROM_RESPONSE_LIKE_SSI = getattr(
    settings, 'USE_RENDER_FROM_RESPONSE_LIKE_SSI', True)
DEFAULT_TEMPLATE = getattr(settings, 'DEFAULT_TEMPLATE', 'default.html')

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
