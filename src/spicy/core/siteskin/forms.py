from django import forms
from django.conf import settings
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
from django.contrib.contenttypes.generic import generic_inlineformset_factory
from django.core.cache import cache
from django.utils.encoding import smart_unicode
from django.utils.safestring import SafeUnicode
from django.utils.translation import ugettext_lazy as _


class ValueAndHiddenInput(forms.HiddenInput):
    def render(self, name, value, attrs=None):
        original = super(ValueAndHiddenInput, self).render(name, value, attrs)
        if value is not None:
            return SafeUnicode(original + smart_unicode(value))
        else:
            return original

