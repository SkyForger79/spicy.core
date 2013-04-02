from django.conf import settings
from django.contrib.sites.models import Site, SITE_CACHE

from spicy.core.siteskin.decorators import JsonResponse
from spicy.core.siteskin.exceptions import AjaxException, Ajax404
from spicy.core.siteskin.exceptions import AjaxDataException

class AjaxMiddleware:
    def process_exception(self, request, exception):
        if not isinstance(exception, AjaxException):
            return None
        if isinstance(exception, AjaxDataException):
            return JsonResponse(exception.data)
        if isinstance(exception, Ajax404):
            return JsonResponse({'error': {'type': 404, 'message': exception.message}})


# XXX deprecated. remove
class SiteSkinDetectionMiddleware(object):
    def process_request(self, request):
        current_site = None

        host = request.get_host()#META.get('HTTP_HOST')
        if host:  
            for site in SITE_CACHE.values():
                if site.domain == host:
                    current_site = site
                    break
            if current_site is None:
                try:
                    current_site = Site.objects.get(domain=host)
                    SITE_CACHE[current_site.id] = current_site
                except Site.DoesNotExist:
                    settings.SITE_THREAD_INFO.SITE_ID = 1
                    current_site = Site.objects.get_current()
                
        settings.SITE_THREAD_INFO.SITE_ID = current_site.id
        
        settings.SITE_THREAD_INFO.SKIN_TEMPLATE_DIR = current_site.domain
        request.site = current_site


