# coding: utf-8
from django.conf.urls import patterns, url, include

from spicy.core.siteskin import defaults


public_urls = patterns(
    'spicy.core.${APPNAME}.views',
    url(r'^${APPNAME}/(?P<test_param>[\w\-_.]+)/$', 'profile', name='index'),
)

admin_urls = patterns(
    'spicy.core.${APPNAME}.admin',
    url(r'^main/$', 'main', name='main'),
)


urlpatterns = patterns('',
    url(r'^admin/${APPNAME}/', include(admin_urls, namespace='admin')),)
urlpatterns += patterns('',
    url(r'^', include(public_urls, namespace='public')),)
