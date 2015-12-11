from django import forms
from spicy.utils.models import get_custom_model_class
from django.utils.encoding import smart_unicode
from django.utils.safestring import SafeUnicode
from django.utils.translation import ugettext_lazy as _

from . import defaults, utils

SiteskinModel = get_custom_model_class(defaults.SITESKIN_SETTINGS_MODEL)


class ValueAndHiddenInput(forms.HiddenInput):
    def render(self, name, value, attrs=None):
        original = super(ValueAndHiddenInput, self).render(name, value, attrs)
        if value is not None:
            return SafeUnicode(original + smart_unicode(value))
        else:
            return original


class ThemeForm(forms.ModelForm):
    theme = forms.CharField(
        label=_('Theme'),
        widget=forms.Select(
            attrs={'class': 'uniform'}, choices=utils.get_siteskin_themes()),
        required=True)

    class Meta:
        model = SiteskinModel
        exclude = ('site', )
