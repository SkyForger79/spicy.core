import sys
from django.conf import settings


def reload_server(sender, instance, signal, **kwargs):
    try:
        import uwsgi
        uwsgi.reload()
    except ImportError:
        urlconf = settings.ROOT_URLCONF

        if urlconf in sys.modules:
            reload(sys.modules[urlconf])
