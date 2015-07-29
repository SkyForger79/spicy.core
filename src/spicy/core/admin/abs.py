from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseRedmineSettings(models.Model):
    redmine_tracker_url = models.CharField(
        _('Redmin tracker URL'), max_length=255, blank=True)
    redmine_username = models.CharField(
        _('Redmine username'), max_length=100, blank=True)
    redmine_password = models.CharField(
        _('Redmine password'), max_length=100, blank=True)
    redmine_project = models.CharField(
        _('Redmine project'), max_length=255, blank=True)

    class Meta:
        abstract = True
