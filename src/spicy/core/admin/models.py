from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django.contrib.sites.models import Site
from spicy.core.siteskin.utils import get_siteskin_themes
from spicy.core.siteskin.defaults import DEFAULT_THEME

from . import defaults


class AdminApp(models.Model):
    """                                                                                                                                                                                                  
    register all apps from INSTALLED_APPS and                                                                                                                                                            
    """

    name = models.CharField(_('Store key or URL'), max_length=255)
    description = models.TextField(_('Admins emails'), blank=True)
    homepage =  models.CharField(_('Homepage'), max_length=255)
    version = models.CharField(_('Version'), max_length=30)

    # get `store` param to check new updates throught marketplace.spicycms.com API  
    license_pub_key = models.CharField(_('User license public key'), max_length=255)    
    download_url =  models.CharField(_('Download URL'), max_length=255)
    last_update = models.DateTimeField(_('Last Update'), auto_now=True)

    site = models.ForeignKey(Site)

    class Meta:
        permissions = (
            ('admin_apps', 'Can edit site settings'),
        )
        db_table = 'spicy_apps'
        abstract = True


class Settings(models.Model):
    license_pub_key = models.CharField(_('User license public key'), max_length=255, blank=True)
    sentry_key = models.CharField(_('Sentry key'), max_length=255, blank=True)    

    redmine_key = models.CharField(_('Redmine key'), max_length=255, blank=True)
    redmine_project = models.CharField(_('Redmine project URL'), max_length=255, blank=True)

    # developer mode
    # get developer settings from main server using API call and licence_pub_key
    # ftp access data
    # manager_link
    # 

    admins_emails = models.TextField(_('Admins emails'), blank=True)
    managers_emails = models.TextField(_('Managers emails'), blank=True)

    #notify_50x
    #notify_404
    
    site = models.ForeignKey(Site)

    class Meta:
        permissions = (
            ('edit_settings', 'Can edit site settings'),
        )
        db_table = 'spicy_settings'
        abstract = False

"""
TODO or not TODO ???
is it dublication of simple content block functionality?

class CustomVariable(models.Model):
    name =  models.CharField(
        _('Custom variable name'),
        max_length=100)

    sentry_key = models.CharField(_('Sentry key'), max_length=255)
    redmine_key = models.CharField(_('Redmine key'), max_length=255)
    redmine_project = models.CharField(_('Redmine project URL'), max_length=255)

    admins_emails = models.TextField(_('Admins emails'), blank=True)
    managers_emails = models.TextField(_('Managers emails'), blank=True)

    site = models.ForeignKey(Site)

    class Meta:
        permissions = (
            ('edit_settings', 'Can edit site settings'),
        )
        db_table = 'spicy_settings'
        abstract = True
"""
