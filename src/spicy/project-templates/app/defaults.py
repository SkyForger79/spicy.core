# coding: utf-8
"""${APPNAME_CLASS} default settings."""
from django.conf import settings


CUSTOM_VARIABLE = gettattr(settings, 'CUSTOM_VARIABLE', 1)
