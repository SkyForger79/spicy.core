from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import conf


class AdminApp(models.Model):
    """
    Register all Spicy apps from INSTALLED_APPS and
    """
    order_lv = models.PositiveSmallIntegerField(_('Order lv.'), default=100)
    name = models.CharField(_('Store key or URL'), max_length=255)
    description = models.TextField(_('Admins emails'), blank=True)
    homepage = models.CharField(_('Homepage'), max_length=255)
    version = models.CharField(_('Version'), max_length=30)
    enable_dashboard = models.BooleanField(
        _('Enable dashboard'), default=False)
    enable_quick_add = models.BooleanField(
        _('Enable quick create'), default=False)
    # get `store` param to check new updates throught marketplace.spicycms.com
    # API
    license_pub_key = models.CharField(
        _('User license public key'), max_length=255)
    download_url = models.CharField(_('Download URL'), max_length=255)
    last_update = models.DateTimeField(_('Last Update'), auto_now=True)

    site = models.ForeignKey(Site)

    def label(self):
        return conf.admin_apps_register[self.name]

    def get_version(self):
        raise NotImplemented

    def already_updated(self):
        # TODO api call
        return False

    def update_url(self):
        # {{ app.download_url }}/{{ app.license_pub_key }}
        # Api call
        return None

    def update(self):
        raise NotImplemented

    class Meta:
        permissions = (
            ('admin_apps', 'Can edit site settings'),
        )
        db_table = 'spicy_apps'


class Settings(models.Model):
    @staticmethod
    def get_robots_default():
        site = Site.objects.get_current()
        return (
            "# robots.txt for http://" + site.domain + "\n"
            "User-agent: *\n"
            "Host: " + site.domain + "\n"
            "Sitemap: http://" + site.domain + "/sitemap.xml")

    robots = models.TextField(
        max_length=3000, blank=True, verbose_name=_('robots.txt'),
        default=lambda: Settings.get_robots_default())
    license_pub_key = models.CharField(
        _('User license public key'), max_length=255, blank=True)
    sentry_key = models.CharField(
        _('Sentry key'), max_length=255, blank=True)
    redmine_key = models.CharField(
        _('Redmine key'), max_length=255, blank=True)
    redmine_project = models.CharField(
        _('Redmine project URL'), max_length=255, blank=True)
    ga_key = models.CharField(
        _('Google Analytics API key'), max_length=15, blank=True)

    # developer mode
    # get developer settings from main server using API call and
    # licence_pub_key
    # ftp access data
    # manager_link

    enable_debug_toolbar = models.BooleanField(
        _('Enable DEBUG toolbar'), default=False)
    debug_mode = models.BooleanField(_('DEBUG mode'), default=False)
    admins_emails = models.TextField(_('Admins emails'), blank=True)
    managers_emails = models.TextField(_('Managers emails'), blank=True)

    #notify_50x
    #notify_404
    
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), default=Site.objects.get_current,
        unique=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

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
