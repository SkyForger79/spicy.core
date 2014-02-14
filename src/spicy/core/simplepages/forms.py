from django import forms
from spicy import utils
from . import defaults


class SimplePageForm(forms.ModelForm):
    def clean_url(self):
        value = self.cleaned_data['url']
        if value and not value.startswith('/'):
            value = '/' + value
        return value

    class Meta:
        model = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)
        fields = (
            'title', 'url', 'content', 'enable_comments', 'is_custom',
            'registration_required', 'sites', 'template_name')
        widgets = {'is_custom': forms.HiddenInput()}
