from django.conf.urls.defaults import patterns, url, include

from spicy.core.siteskin import defaults
from spicy.core.service import api

public_urls = patterns('')

admin_urls = patterns(
    'spicy.core.service.admin',
    url(r'^$', 'index', name='index'),
    url(r'^services/$', 'services', name='services'),
)    

admin_urls += api.register.urls()
public_urls += api.register.urls(is_public=True)

urlpatterns = patterns('',)
if defaults.USE_CUSTOM_ADMIN:
    urlpatterns += patterns(url(r'^admin/', include(admin_urls, namespace='admin')),)

urlpatterns += patterns(url(r'^', include(public_urls, namespace='public')),)
