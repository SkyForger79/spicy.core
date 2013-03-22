from django.conf.urls.defaults import patterns, url, include


admin_urls = patterns(
    'spicy.core.admin.views',
#    url(r'^$', 'index', name='index'),
    url(r'^login/$', 'login', name='login'),
)

urlpatterns = patterns('',)

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin_urls)),
)
