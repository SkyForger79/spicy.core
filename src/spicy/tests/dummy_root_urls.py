from django.conf.urls import url, include

import spicy.core.profile.urls as profile_urls
import spicy.core.service.urls as service_urls

urlpatterns = [
    url(r'^profile/', include(profile_urls, namespace='profile')),
    url(r'^service/', include(service_urls, namespace='service')),
]
