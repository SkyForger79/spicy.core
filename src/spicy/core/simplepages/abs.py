from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractBasePage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(
        _('content'), blank=True,
        default=(
            '{% block content %}\n<!-- Page content here-->\n'
            '{% endblock %}'))
    template_name = models.CharField(
        _('template name'), max_length=70, blank=True,
        default='spicy.core.simplepages/default.html',
        help_text=_(
            "Example: 'contact_page.html'. If this isn't "
            "provided, the system will use "
            "'spicy.core.simplepages/default.html'."))
    sites = models.ManyToManyField('sites.Site')

    class Meta:
        abstract = True
        db_table = 'sp_simplepage'
        verbose_name = _('simple page')
        verbose_name_plural = _('simple pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url


class AbstractSimplePage(AbstractBasePage):
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_(
            "If this is checked, only logged-in users will be able to view "
            "the page."),
        default=False)

    class Meta(AbstractBasePage.Meta):
        abstract = True
