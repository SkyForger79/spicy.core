from django.conf.urls import patterns, url, include
from django.conf import settings
# from django.views.static import serve


admin_urls = patterns(
    'spicy.core.admin.views',

    url(r'^login/$', 'login', name='login'),
)

urlpatterns = patterns('',
     url(r'^admin/', include(admin_urls, namespace='admin')),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         url(r'^%s(?P<path>.*)$' % settings.STATIC_ROOT.lstrip('/'),
#             serve, {
#                 'document_root': settings.STATIC_ROOT
#             }
#         ),
#     )

from django.conf.urls.static import static

urlpatterns += patterns('',
    # ... the rest of your URLconf goes here ...
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
