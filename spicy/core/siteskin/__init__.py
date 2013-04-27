from . import defaults
from django.core.cache import get_cache


cache = get_cache(defaults.SITESKIN_CACHE_BACKEND)
