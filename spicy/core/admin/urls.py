from django.conf.urls.defaults import patterns, url, include

from spicy.core.service import api


urlpatterns = patterns(
    'spicy.core.admin.views',
    url(r'^$', 'index', name='index'),
)    
