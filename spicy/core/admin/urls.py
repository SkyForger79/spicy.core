from django.conf.urls import patterns, url, include
from django.conf import settings
from django.conf.urls.static import static


admin_urls = patterns(
    'spicy.core.admin.views',

    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

urlpatterns = patterns('',
     url(r'^admin/', include(admin_urls, namespace='admin')),
)
