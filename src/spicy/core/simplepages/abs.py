from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Template
from spicy.core.trash.models import MultiSitesTrashModel


class EditableTemplateModel(models.Model):
    content = models.TextField(
        _('Page Source'), blank=True,
        default=(
            '{% extends current_base %}\n'
            '{% block content %}\n<!-- Page content here-->\n'
            '{% endblock %}'))
    template_name = models.CharField(
        _('template name'), max_length=255, blank=True, default='')
    is_custom = models.BooleanField(_('Is custom'))

    def get_main_content(self):
        # For spicy.seo
        if self.is_custom:
            return self.content
        else:
            content = ''
            if loader.template_source_loaders:
                for template_loader in loader.template_source_loaders:
                    try:
                        content = template_loader.load_template_source(
                            self.template_name)[0]
                        break
                    except Exception:
                        continue
            return content

    def get_template(self):
        return (
            Template(self.content) if self.is_custom else
            loader.get_template(self.template_name))

    class Meta:
        abstract = True


class AbstractSimplePage(EditableTemplateModel, MultiSitesTrashModel):
    sites = models.ManyToManyField('sites.Site')
    url = models.CharField(
        _('URL'), max_length=100, db_index=True, unique=True)
    title = models.CharField(_('title'), max_length=200)
    is_sitemap = models.BooleanField(
        default=False, verbose_name=_('Do not add this page to sitemap.xml'))
    is_active = models.BooleanField(
        default=False, verbose_name=_('Do not show page visitors'))
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_(
            "If this is checked, only logged-in users will be able to view "
            "the page."),
        default=False)

    class Meta(EditableTemplateModel.Meta):
        abstract = True
        db_table = 'sp_simplepage'
        verbose_name = _('Simple page')
        verbose_name_plural = _('Simple pages')
        ordering = ('url',)
        permissions = [('change_robots_txt', 'Robots.txt')]

    def __unicode__(self):
        return u"{0} -- {1}".format(self.url, self.title)

    def get_absolute_url(self):
        return self.url
