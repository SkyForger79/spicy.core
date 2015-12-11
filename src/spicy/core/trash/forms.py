from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory

from django.contrib.sites.models import Site

class TrashFiltersForm(forms.Form):
    # TODO group by ContentTypes or Apps
    consumer_type = forms.ModelChoiceField(
        label=_('ContentType'), queryset=ContentType.objects.all(), required=False)
    consumer_type.widget.attrs['class'] = 'uniform'

    search_text = forms.CharField(max_length=100, required=False)
