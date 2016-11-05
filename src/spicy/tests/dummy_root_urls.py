from django.conf.urls import url, include

import spicy.core.profile.urls as profile_urls

urlpatterns = [
    url(r'^', include(profile_urls, namespace='profile')),
]
