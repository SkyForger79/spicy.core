from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings


admin_urls = patterns(
    'spicy.core.admin.views',

    url(r'^login/$', 'login', name='login'),
)

urlpatterns = patterns('',
     url(r'^admin/', include(admin_urls, namespace='admin')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
