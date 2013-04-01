import os, sys
from config.local import ADDITIONAL_PYTHON_PATH

PROJECT_ROOT = os.path.abspath('.')
sys.path.append(os.path.abspath('./apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ADDITIONAL_PYTHON_PATH))

os.environ['DJANGO_SETTINGS_MODULE'] = 'apps.settings'

from django.conf import settings
from spicy.core.service import api

for service_path in settings.SERVICES:
    api.register.add(service_path)
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
