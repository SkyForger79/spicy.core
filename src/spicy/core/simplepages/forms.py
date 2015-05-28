from django import forms, http, template
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django import get_version as django_version
from spicy import utils
from spicy.core.admin.conf import admin_apps_register
from . import defaults


class EditableTemplateForm(forms.ModelForm):
    def clean_template_name(self):
        value = self.cleaned_data['template_name']
        if not self.cleaned_data['is_custom'] and not value:
            raise forms.ValidationError(
                _("Can't save a page without template"))
        return value

    def clean_content(self):
        content = self.cleaned_data['content']

        if not content and self.cleaned_data['is_custom']:
            template_name = self.cleaned_data['template_name']
            for template_loader in loader.template_source_loaders:
                try:
                    content = template_loader.load_template_source(
                        template_name)[0]
                    break
                except Exception:
                    continue

        if django_version() > '1.5':
            from django.test.client import RequestFactory
            request = RequestFactory().get('/')
        else:
            request = http.HttpRequest()
        request.session = {}
        context = template.RequestContext(
            request,
            {'page_slug': self.instance.title, 'page': self.instance})
        if content:
            try:
                template.Template(content).render(context)
            except Exception:
                import traceback; traceback.print_exc()
                raise forms.ValidationError(_("Template error detected"))
        return content


class SimplePageForm(EditableTemplateForm):
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

    class Meta:
        model = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)
        fields = (
            'title', 'url',  'is_custom',  'template_name', 'content',
            'enable_comments', 'is_active', 'registration_required', 'sites',
            'is_sitemap')
        widgets = {'is_custom': forms.HiddenInput()}
