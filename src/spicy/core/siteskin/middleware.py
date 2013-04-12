import json
from django.conf import settings

from spicy.core.siteskin.decorators import JsonResponse
from spicy.core.siteskin.exceptions import AjaxException, Ajax404
from spicy.core.siteskin.exceptions import AjaxDataException

class AjaxMiddleware(object):
    def process_request(self, request):
        request.json = dict()
        if request.method == 'POST' and request.is_ajax():
            if request.body:
                if request.META['CONTENT_TYPE'].startswith(
                    'application/x-www-form-urlencoded'):
                    request.json = request.POST.copy()
                else:
                    request.json = json.loads(request.body)


    def process_exception(self, request, exception):
        if not isinstance(exception, AjaxException):
            return None
        if isinstance(exception, AjaxDataException):
            return JsonResponse(exception.data)
        if isinstance(exception, Ajax404):
            return JsonResponse({'error': {'type': 404, 'message': exception.message}})

