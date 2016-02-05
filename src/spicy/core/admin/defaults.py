# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

ADMIN_THEME = getattr(settings, 'ADMIN_THEME', None)
THEMES_PATH = getattr(settings, 'THEMES_PATH', os.path.abspath('../'))
SPICY_THEME_FILE = getattr(settings, 'SPICY_THEME_FILE', 'spicy.theme')
SPICY_THEME_PRODUCT_KEYS = getattr(
    settings, 'SPICY_THEME_PRODUCT_KEYS', ['spicy.light', 'spicy.media', 'spicy.ecom'])

DEBUG_ADMIN = getattr(settings, 'DEBUG_ADMIN', settings.DEBUG)

USE_CUSTOM_ADMIN = getattr(settings, 'USE_CUSTOM_ADMIN', True)
ADMIN_OBJECTS_PER_PAGE = getattr(settings, 'ADMIN_OBJECTS_PER_PAGE', 50)

ADMIN_APPS = getattr(settings, 'ADMIN_APPS', [])
ADMIN_DASHBOARD_APPS = getattr(settings, 'ADMIN_DASHBOARD_APPS', [])

ADMIN_CUSTOM_SETTINGS_MODEL = getattr(settings, 'ADMIN_CUSTOM_SETTINGS_MODEL', 'admin.Settings')

# App order for default page. If app and namespace name don't match, item
# should be a pair of (namespace , app).
APP_ORDER = getattr(
    settings, 'APP_ORDER', 
    ('presscenter', 'mediacenter', 'labels', 'profile', 'service', 'siteskin')
    )

ADMIN_APP_CREATE_LABELS = getattr(settings, 'ADMIN_APP_CREATE_LABELS', {
        'profile': _('Account'),
        })

