from django.conf.urls.defaults import *

public_urls = patterns(
    'spicy.core.trash.views',
    )

admin_urls = patterns(
    'spicy.core.trash.admin',
    url(r'^$', 'index', name='index'),
    url(r'^restore/(?P<provider_id>\d+)/$', 'restore', name='restore'),
    )

urlpatterns = patterns('',
    url(r'^admin/trash/', include(admin_urls, namespace='admin')),
    url(r'^trash/', include(public_urls, namespace='public'))
    )
