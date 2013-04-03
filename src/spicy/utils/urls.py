from django.conf import settings
from django.conf.urls.defaults import include, patterns, url


def add_optional_urls(urlpatterns, apps, app_namespace='spicy.'):
    for app in apps:        
        full_app_name = '%s%s' % (app_namespace, app)
        if full_app_name in settings.INSTALLED_APPS:
            urlpatterns += patterns(
                '',
                url(r'^%s/' % app, include(full_app_name + '.urls', namespace=app)))
