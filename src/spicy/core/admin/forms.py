from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms
from spicy.utils.models import get_custom_model_class
from spicy.core.siteskin.utils import get_siteskin_themes
from django.contrib.sites.models import Site

from . import defaults

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)

# TODO SiteForm

class SettingsForm(forms.ModelForm):    
    class Meta:
        model = SettingsModel
        fields = ('admins_emails', 'managers_emails',)


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        fields = ('sentry_key', 'redmine_key', 'redmine_project', 
                  'enable_debug_toolbar', 'debug_mode')


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        fields = ('license_pub_key', )


class RobotsForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        fields = ('robots',)


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('name', 'domain') 
