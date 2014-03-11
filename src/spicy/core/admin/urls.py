from django.conf.urls import patterns, url, include


admin_urls = patterns(
    'spicy.core.admin.admin',
    url(r'^$', 'dashboard', name='index'),
    url(r'^settings/main/$', 'main_settings', name='settings'),
    url(r'^settings/robots/$', 'robots_txt', name='robots'),
    url(r'^settings/sitemap/$', 'sitemap', name='sitemap'),
    url(r'^settings/managers/$', 'managers', name='managers'),
    url(r'^settings/developer/$', 'developer', name='developer'),
    url(r'^settings/application/$', 'application', name='application'),
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
    url(r'^robots.txt$', 'spicy.core.admin.views.robots'),
)
