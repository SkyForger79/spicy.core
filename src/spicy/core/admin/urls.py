from django.conf.urls import patterns, url, include
from django.conf import settings


admin_urls = patterns(
    'spicy.core.admin.admin',
    url(r'^$', 'dashboard', name='index'),
    url(r'^settings/$', 'edit_settings', name='settings'),
    url(r'^developer/$', 'developer', name='developer'),
    url(r'^application/$', 'application', name='application'),
)

public_urls = patterns(
    'spicy.core.admin.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin_urls, namespace='admin')),
    url(r'^admin/', include(public_urls, namespace='public')),
)
