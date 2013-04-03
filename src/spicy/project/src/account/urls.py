from django.conf.urls.defaults import include, patterns, url

public_urls = patterns(
    'account.views',
    url(r'^account/(?P<account_id>\d+)/$', 'view', name='view'),
    url(r'^delete/(?P<account_id>\d+)/$', 'delete', name='delete'),
)

urlpatterns = patterns(
    '',
    url(r'^', include(public_urls, namespace='public'))
)
