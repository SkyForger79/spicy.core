from django.conf.urls import patterns, url, include

from . import defaults

public_urls = patterns(
    '',
    url(r'^$', defaults.SITESKIN_INDEX_VIEW,
        {'template': 'index.html', 'page_slug': 'index'},
        name='index'),
)

public_urls += patterns(
    'spicy.core.siteskin.views',

    url(r'^robots.txt$', 'render',
        {'template': 'robots.txt', 'mimetype': 'text/plain'},
        name='robots.txt'),

)

admin_urls = patterns(
    'spicy.core.siteskin.admin',
    )


urlpatterns = patterns('',)
if defaults.USE_CUSTOM_ADMIN:
    urlpatterns += patterns(
        '',
        url(r'^admin/siteskin/', include(admin_urls, namespace='admin')),
)

urlpatterns += patterns(
    '',
    url(r'^', include(public_urls, namespace='public')),
    )
