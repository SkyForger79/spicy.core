from django import forms
from .. import defaults
from .html import Sanitizer


if defaults.SANITIZE_DOCUMENTS:
    sanitizer = Sanitizer(
        allowed_elements=defaults.ALLOWED_HTML_ELEMENTS,
        allowed_attributes=defaults.ALLOWED_HTML_ATTRIBUTES,
        allowed_classes=defaults.ALLOWED_HTML_CLASSES,
        escape_invalid_tags=defaults.ESCAPE_INVALID_TAGS,
        strip_whitespace=False)

    class SanitizingCharField(forms.CharField):
        def clean(self, value):
            return sanitizer.sanitize(
                super(SanitizingCharField, self).clean(value))

else:
    SanitizingCharField = forms.CharField
