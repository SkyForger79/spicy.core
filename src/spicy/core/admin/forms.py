from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import forms
from spicy.utils.models import get_custom_model_class
from spicy.core.siteskin.utils import get_siteskin_themes

from . import defaults

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)

class SettingsForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        exclude = ('site', )


class DeveloperForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        exclude = ('site', )


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
        exclude = ('site', )
