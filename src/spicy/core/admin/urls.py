from django.conf.urls import patterns, url, include
from django.conf import settings


admin_urls = patterns(
    'spicy.core.admin.views',

    url(r'^login/$', 'login', name='login'),
)

urlpatterns = patterns('',
     url(r'^admin/', include(admin_urls, namespace='admin')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT
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
#     urlpatterns += patterns('',
#         url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
#             'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
#     )
# else:
#     urlpatterns = ('')
#
#
# if settings.DEBUG:
#     public_urls = patterns(
#         url(r'^%s(?P<path>.*)$' % defaults.MEDIACENTER_URL,
#             django.views.static.serve,
#             {'document_root': defaults.MEDIACENTER_ROOT}))
# else:
#     public_urls = patterns('')
#
#
# urlpatterns = patterns(
#     '',
#     url(r'^admin/', include(admin_urls, namespace='admin')),
# )
#
#
#
