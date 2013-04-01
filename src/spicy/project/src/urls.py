from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
from spicy import utils


handler404 = 'spicy.core.siteskin.views.page_not_found'
handler500 = 'spicy.core.siteskin.views.server_error'
handler403 = 'spicy.core.siteskin.views.forbidden'

from django.contrib.flatpages.models import FlatPage

urlpatterns = patterns('',)

# flatpages
for page in FlatPage.objects.filter(sites__id__exact=settings.SITE_ID):
    urlpatterns += patterns(
        'spicy.core.siteskin.views',
        url(r'^%s$' % page.url.lstrip('/'), 'render',
            {'template': page.template_name, 'page': page},
            name=page.template_name),
        )

urlpatterns += patterns(
    '',
    #url(r'^admin/$', 'spicy.core.profile.admin.main'),
    url(r'^', include('spicy.core.siteskin.urls', namespace='index')),

    url(r'^', include('spicy.core.service.urls', namespace='service')), 
    url(r'^', include('spicy.core.profile.urls', namespace='profile')),
    #url(r'^', include('spicy.apps.mediacenter.urls', namespace='mediacenter')),
    #url(r'^', include('spicy.apps.presscenter.urls', namespace='presscenter')),
    #url(r'^', include('spicy.apps.categories.urls', namespace='categories')),

    url(r'^', include('account.urls', namespace='account')),


    )


#utils.add_optional_urls(
#    urlpatterns, ['feedback', 'bookmarks', ])


if settings.DEBUG:

    urlpatterns += patterns(
        '',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
			'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^%s(?P<path>.*)$' % settings.MEDIACENTER_URL.lstrip('/'),
			'django.views.static.serve',
            {'document_root': settings.MEDIACENTER_ROOT}),
    )


urlpatterns += patterns(
    '',
    url(r'^captcha/', include('captcha.urls')),
    # jsi18n localization #(?P<packages>\S+?)/
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    )

# Flatpages must be included last.
#urlpatterns += patterns('',
#  url(r'^', include('django.contrib.flatpages.urls', namespace='flatpages')),  
#)
