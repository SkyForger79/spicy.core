__import__('pkg_resources').declare_namespace(__name__)

from spicy.core.siteskin import defaults
from django.core.cache import get_cache


cache = get_cache(defaults.SITESKIN_CACHE_BACKEND)
