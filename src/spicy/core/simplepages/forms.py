from django import forms, http, template
from django.utils.translation import ugettext_lazy as _
from spicy import utils
from spicy.core.admin.conf import admin_apps_register
from . import defaults


class SimplePageForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        seo = super(SimplePageForm, self).save(*args, **kwargs)
        if 'spicy.seo' in admin_apps_register.keys():
            if not seo.og_title:
                seo.og_title = seo.title
            if not seo.seo_title:
                seo.seo_title = seo.title
            if not seo.og_url:
                seo.og_url = seo.get_absolute_url()
            seo.save()
        return seo

    def clean_url(self):
        value = self.cleaned_data['url']
        if value and not value.startswith('/'):
            value = '/' + value
        return value

    def clean_template_name(self):
        value = self.cleaned_data['template_name']
        if not self.cleaned_data['is_custom'] and not value:
            raise forms.ValidationError(
                _("Can't save a page without template"))
        return value

    def clean_content(self):
        content = self.cleaned_data['content']
        context = template.RequestContext(
            http.HttpRequest(),
            {'page_slug': self.instance.title, 'page': self.instance})
        if content:
            try:
                template.Template(content).render(context)
            except Exception:
                raise forms.ValidationError(_("Template error detected"))
        return content

    class Meta:
        model = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)
        fields = (
            'title', 'url', 'content', 'enable_comments', 'is_custom',
            'is_active', 'registration_required', 'sites', 'template_name',
            'is_sitemap')
        widgets = {'is_custom': forms.HiddenInput()}
