# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEBUG_ADMIN = getattr(settings, 'DEBUG_ADMIN', settings.DEBUG)

USE_CUSTOM_ADMIN = getattr(settings, 'USE_CUSTOM_ADMIN', True)
ADMIN_OBJECTS_PER_PAGE = getattr(settings, 'ADMIN_OBJECTS_PER_PAGE', 50)

ADMIN_APPS = getattr(settings, 'ADMIN_APPS', [])
ADMIN_DASHBOARD_APPS = getattr(settings, 'ADMIN_DASHBOARD_APPS', [])

ADMIN_SETTINGS_MODEL = getattr(
    settings, 'ADMIN_SETTINGS_MODEL', 'admin.Settings')

# App order for default page. If app and namespace name don't match, item
# should be a pair of (namespace , app).
APP_ORDER = getattr(
    settings, 'APP_ORDER',
    ('presscenter', 'mediacenter', 'labels', 'profile', 'service', 'siteskin')
)

ADMIN_APP_CREATE_LABELS = getattr(
    settings, 'ADMIN_APP_CREATE_LABELS', {'profile': _('Account')})

DASHBOARD_LISTS_LENGTH = getattr(settings, 'DASHBOARD_LISTS_LENGTH', 5)

CRM_BACKENDS = getattr(settings, 'CRM_BACKENDS', ())
