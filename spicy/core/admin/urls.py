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

if settings.DEBUG:
    print settings.STATIC_ROOT.lstrip('/')

    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % settings.STATIC_ROOT.lstrip('/'),
            'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT
            }
        ),
    )

#
# admin_urls = patterns(
#     'spicy.core.admin.views',
# #    url(r'^$', 'index', name='index'),
#     url(r'^login/$', 'login', name='login'),
#
#     url(r'^snippets/add-new-item', 'add_new_item', name='add_new_item')
# )
#
# if settings.DEBUG:
    urlpatterns += patterns('') + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
