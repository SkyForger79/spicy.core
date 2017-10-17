from django.conf.urls import url, include, patterns

import spicy.core.admin.urls as admin_urls
import spicy.core.profile.urls as profile_urls
import spicy.core.service.urls as service_urls

urlpatterns = [
    url(r'^admin/', include(admin_urls, namespace='admin')),
    url(r'^profile/', include(profile_urls, namespace='profile')),
    url(r'^service/', include(service_urls, namespace='service')),
]

urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)
