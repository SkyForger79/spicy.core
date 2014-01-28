from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.contrib.sites.models import Site
from spicy.core.siteskin.utils import get_siteskin_themes

from . import defaults


class Siteskin(models.Model):
    theme = models.CharField(
        _('Theme'),
        choices=get_siteskin_themes(),
        default=defaults.DEFAULT_THEME,
        max_length=255)

    admin_obj_per_page = models.PositiveSmallIntegerField(_('Admin obj per page'), default=50)
    site_obj_per_page = models.PositiveSmallIntegerField(_('Site obj per page'), default=20)
    
    site = models.ForeignKey(Site)

    class Meta:
        permissions = (
            ('edit_siteskin', 'Can edit site settings'),
        )
        db_table = 'spicy_siteskin'
        abstract = False
