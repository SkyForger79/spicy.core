from . import models
from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


class ServiceForm(forms.ModelForm):
    site = forms.ModelMultipleChoiceField(
        label=_('Sites'), required=True,
        widget=forms.SelectMultiple(attrs={'class': 'SelectMultiple'}),
        queryset=Site.objects.all())

    class Meta:
        model = models.Service
        exclude = ('name', 'date_joined', 'is_default', 'description')


class ProviderCreateForm(forms.ModelForm):
    # TODO: refactoring
    # def save(self, *args, **kwargs):
#         provider = self._meta.model.objects.create(
#             service=self.cleaned_data['service'],
#             consumer_id=self.cleaned_data['consumer_id'],
#             consumer_type=self.cleaned_data['consumer_type'])
#         return provider

    class Meta:
        model = models.ProviderModel
        fields = ('service', 'consumer_id', 'consumer_type')


class ProviderForm(forms.ModelForm):
    class Meta:
        model = models.ProviderModel


class ContentProviderForm(forms.ModelForm):
    template = forms.ChoiceField(
        label=_('Template'), choices=())

    def __init__(self, *args, **kwargs):
        super(ContentProviderForm, self).__init__(*args, **kwargs)

        from spicy.core.service import api

        self.fields['template'].choices = \
            api.register[self.instance.service.name].content_templates

    class Meta:
        model = models.ContentProviderModel


class BillingProviderForm(forms.ModelForm):
    class Meta:
        model = models.BillingProviderModel
        exclude = ('date_joined',)
        widgets = {
            #'service': forms.widgets.HiddenInput(),
            'consumer_id': forms.widgets.HiddenInput(),
            'consumer_type': forms.widgets.HiddenInput(),
            }
