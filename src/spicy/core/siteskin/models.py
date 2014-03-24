from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.core.siteskin.utils import get_siteskin_themes
from . import defaults
from spicy.core.simplepages import defaults as sp_defaults
from spicy.utils.models import get_custom_model_class

SimplePage = get_custom_model_class(sp_defaults.SIMPLE_PAGE_MODEL)

class Siteskin(models.Model):
    theme = models.CharField(
        _('Theme'), choices=get_siteskin_themes(),
        default=defaults.DEFAULT_THEME, max_length=255)
    admin_obj_per_page = models.PositiveSmallIntegerField(
        _('Admin obj per page'), default=50)
    site_obj_per_page = models.PositiveSmallIntegerField(
        _('Site obj per page'), default=20)
    site = models.ForeignKey(Site)
    home_page = models.ForeignKey(sp_defaults.SIMPLE_PAGE_MODEL, verbose_name=_('Home Page'))

    class Meta:
        permissions = (
            ('edit_siteskin', 'Can edit site settings'),
        )
        db_table = 'spicy_siteskin'
        abstract = False
