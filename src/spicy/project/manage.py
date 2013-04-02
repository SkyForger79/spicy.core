#!/usr/bin/env python                                                                                                                                            
from django.core.management import execute_manager
import site, os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings'

from django.conf import settings

try:
    from src import settings
except ImportError, msg:
    import sys
    sys.stderr.write('%s' % msg)
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-a\
dmin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

# Used only with FastCGI implementation
if hasattr(settings, 'VIRTUALENV'):
    site.addsitedir(settings.VIRTUALENV)

if settings.DEBUG:
    # local configuration imports
    try:
        from config import *
    except ImportError, msg:
        print msg
        raise ImportError, style.ERROR('Using default config settings, check "config" directory.\n')

    PROJECT_ROOT = os.path.abspath('.')
    sys.path.insert(0, os.path.join(PROJECT_ROOT, settings.ADDITIONAL_PYTHON_PATH))


from spicy.core.service import api
for service_path in settings.SERVICES:
    api.register.add(service_path)


if __name__ == "__main__":
    execute_manager(settings)

