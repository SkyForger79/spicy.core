import os
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.staticfiles import urls as st_urls
from . import defaults, utils


admin_urls = patterns(
    'spicy.core.siteskin.admin',
    url(r'^edit/$', 'edit', name='edit'),
)

public_urls = patterns(
    '',
    url(r'^$', defaults.SITESKIN_INDEX_VIEW,
        {'template_name': 'index.html', 'page_slug': 'index'}, name='index'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

if settings.DEBUG:
    current_theme = os.path.basename(
        utils.get_siteskin_settings().theme)
    st_urls.urlpatterns = [st_urls.staticfiles_urlpatterns(
        '{}{}/'.format(settings.STATIC_URL, current_theme))]

urlpatterns = patterns(
    '',
    url(r'^admin/siteskin/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)
