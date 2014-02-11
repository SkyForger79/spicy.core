from django import forms
from spicy import utils
from . import defaults


class SimplePageForm(forms.ModelForm):
    class Meta:
        model = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)
        fields = ('title', 'url', 'content', 'enable_comments',
            'registration_required', 'sites', 'template_name')
