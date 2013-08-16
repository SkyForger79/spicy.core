from django.conf import settings
from django.conf.urls import patterns, url, include

from . import defaults

public_urls = patterns(
    '',
    url(r'^$', defaults.SITESKIN_INDEX_VIEW,
        {'template_name': 'index.html', 'page_slug': 'index'}, name='index'),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

public_urls += patterns(
    'spicy.core.siteskin.views',

    url(
        r'^robots.txt$', 'render',
        {'template_name': 'robots.txt', 'mimetype': 'text/plain',
         'noindex': not defaults.ENABLE_INDEXATION},
        name='robots.txt'),
)


urlpatterns = patterns(
    '',
    url(r'^', include(public_urls, namespace='public')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)
