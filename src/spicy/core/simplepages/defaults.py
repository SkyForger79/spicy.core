# -*- coding: utf-8 -*-

from django.conf import settings
#from django.utils.translation import ugettext_lazy as _

USE_DEFAULT_SIMPLE_PAGE_MODEL = getattr(
    settings, 'USE_DEFAULT_SIMPLE_PAGE_MODEL', True)

SIMPLE_PAGE_MODEL = (
    'simplepages.DefaultSimplePage' if USE_DEFAULT_SIMPLE_PAGE_MODEL else
    settings.SIMPLE_PAGE_MODEL)
