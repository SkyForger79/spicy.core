from django.conf import settings
from django.core.cache import get_cache

if settings.configured:
    from spicy.core.siteskin import defaults
    cache = get_cache(defaults.SITESKIN_CACHE_BACKEND)

else:
    from django.core.cache import get_cache
    cache = get_cache('django.core.cache.backends.dummy.DummyCache')

__import__('pkg_resources').declare_namespace(__name__)
