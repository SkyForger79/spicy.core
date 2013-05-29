from django.conf import settings
from django.conf.urls import patterns, url, include

from . import defaults

public_urls = patterns(
    '',
    url(r'^$', defaults.SITESKIN_INDEX_VIEW,
        {'template': 'index.html', 'page_slug': 'index'}, name='index'),
)

public_urls += patterns(
    'spicy.core.siteskin.views',

    url(r'^robots.txt$', 'render',
        {'template': 'robots.txt', 'mimetype': 'text/plain'}, name='robots.txt'),

)


urlpatterns = patterns(
    '',
    url(r'^', include(public_urls, namespace='public')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )


# BUG delete this
# if settings.DEBUG:
#     urlpatterns += patterns(
#         '',
#         url(r'^{0}(?P<path>.*)$'.format(settings.STATIC_ROOT.lstrip('/')),
#             'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

#         url(r'^{0}(?P<path>.*)$'.format(settings.MEDIA_URL.lstrip('/')),
#             'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
                            
#     )
