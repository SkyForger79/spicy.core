from spicy.utils.printing import print_error
from django.conf import settings


#: Used only like stubs during installing and other not-in-work cases
# GENERIC_DEFAULTS = dict(
#     PROJECT_ROOT='~/',
#     CACHES='default',
# )
#
# SITESKIN_DEFAULTS = dict(
#     USE_CUSTOM_ADMIN=True,
#     SITESKIN='example.com',
#     SITESKIN_ADMIN=None,
# )


if not settings.configured:
    # print_error('Error importing Django settings')
    # settings.configure(default_settings=GENERIC_DEFAULTS, **SITESKIN_DEFAULTS)
    settings.configure()



SITESKIN = getattr(settings, 'SITESKIN', 'example.com')
SITESKIN_DEBUG = getattr(settings, 'SITESKIN_DEBUG', settings.DEBUG)
SITESKIN_DEBUG_CODE_LEN = 3

OBJECTS_PER_PAGE = getattr(settings, 'OBJECTS_PER_PAGE', 50)


PAGES_FROM_START = getattr(settings, 'PAGES_FROM_START', 2)
PAGES_TO_END = getattr(settings, 'PAGES_TO_END', 2)

DEBUG_ERROR_PAGES = getattr(settings, 'DEBUG_ERROR_PAGES', False)

USE_RENDER_FROM_RESPONSE_LIKE_SSI = getattr(
    settings, 'USE_RENDER_FROM_RESPONSE_LIKE_SSI', True)
DEFAULT_TEMPLATE = getattr(settings, 'DEFAULT_TEMPLATE', 'default.html')
SITEMAP_URL = getattr(settings, 'SITEMAP_URL', '/')
SITEMAP_GZIP_COMPRESSION = 6  # Must be in 1-9 interval, 1 is fastest.
#MAX_MESSAGE_STRING_LENGTH = 1000

SITESKIN_INDEX_VIEW = getattr(
    settings, 'SITESKIN_INDEX_VIEW', 'spicy.core.siteskin.views.render')
SITESKIN_CACHE_BACKEND = getattr(
    settings, 'SITESKIN_CACHE_BACKEND', 'default')

AJAX_API_STATUS_CODE_SUCCESS = 'success'
AJAX_API_STATUS_CODE_ERROR = 'error'

AJAX_API_VERSION = getattr(settings, 'AJAX_API_VERSION', '0.1-default')


DEFAULT_FILTERS = [
    ('search_text', ''),
]
ENABLE_INDEXATION = getattr(settings, 'ENABLE_INDEXATION', True)
