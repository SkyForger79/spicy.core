from django.conf import settings
from django import forms
from spicy.utils.models import get_custom_model_class

from . import defaults

SettingsModel = get_custom_model_class(defaults.ADMIN_CUSTOM_SETTINGS_MODEL)

class SettingsForm(forms.ModelForm):
    class Meta:
        model = SettingsModel
