from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.contrib.sites.models import Site

from . import defaults, utils


class Settings(models.Model):    
    current_theme =  models.CharField(
        _('Choose theme'), choices=utils.get_themes_from_path(defaults.THEMES_PATH), max_length=255)
    
    head_html = models.TextField(_('HEAD html, for SEO gloabal meta tags and counters'), blank=True)
    footer_html = models.TextField(_('FOOTER html, for counters and not async JS scripts'), blank=True)    

    class Meta:
        permissions = (
            ('edit_settings', 'Can edit site settings'),
        )
        db_table = 'spicy_settings'
        abstract = True
