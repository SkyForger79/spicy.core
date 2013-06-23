from django.conf import settings
from django.conf.urls import patterns, url, include
from . import api

api.register.load_urls()

public_urls = patterns('')

admin_urls = api.register.urls()
public_urls += api.register.urls(is_public=True)

urlpatterns = patterns('',)
urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin_urls, namespace='admin')),
    )

urlpatterns += patterns(
    '',
    url(r'^', include(public_urls, namespace='public')),)
