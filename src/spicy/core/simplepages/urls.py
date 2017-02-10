

from django.conf import settings
from django.conf.urls import patterns, url, include

from spicy.utils import get_custom_model_class
from . import defaults


SimplePage = get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


admin_urls = patterns(
    'spicy.core.simplepages.admin',
    url(r'^$', 'index', name='index'),
    url(r'^create/$', 'create', name='create'),
    url(r'^find/$', 'find', name='find'),
    url(r'^(?P<simplepage_id>\d+)/$', 'edit', name='edit'),
    url(r'^(?P<simplepage_id>\d+)/seo/$', 'edit_seo', name='edit-seo'),
    url(r'^(?P<simplepage_id>\d+)/delete/$', 'delete', name='delete'),
)

urlpatterns = patterns('')

#from django.db import connection
#if 'django_site' in connection.introspection.table_names():
# XXX
# load it only after syncdb and check database exist
for page in SimplePage.objects.filter(sites__id__exact=settings.SITE_ID):
    urlpatterns += patterns(
        'spicy.core.simplepages.views',
        url(r'^%s$' % page.url.lstrip('/'), 'render_simplepage',
            {'page': page},
            name=page.template_name)
    )


urlpatterns += patterns(
    '',
    url(r'^admin/simplepages/', include(admin_urls, namespace='admin')),
#    url(r'^', include(public_urls, namespace='public')),
)
