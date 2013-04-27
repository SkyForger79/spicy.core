# -*- coding: utf-8 -*-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# App order for default page. If app and namespace name don't match, item
# should be a pair of (namespace , app).
APP_ORDER = getattr(
    settings, 'APP_ORDER', 
    ('presscenter', 'mediacenter', 'labels', 'profile', 'service', 'siteskin')
    )

