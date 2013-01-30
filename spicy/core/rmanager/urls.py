from django.conf.urls.defaults import patterns, url, include

public_urls = patterns('')    

admin_urls = patterns('rmanager.admin', 
    url(r'^versions/$', 'versions', name='index'),
    url(r'^memcache/$', 'memcache', name='memcache'),
    url(r'^db-logger/$', 'db_logger', name='db-logger'),
    )


urlpatterns = patterns(
    '',
    url(r'^admin/rmanager/', include(admin_urls, namespace='admin')),
    url(r'^', include(public_urls, namespace='public'))
    )
