from django.core.cache import cache
from django.core.management.color import color_style
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from . import defaults
from spicy.utils import make_cache_key

style = color_style()


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return 
    response with ``application/json`` mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(data, cls=DjangoJSONEncoder), mimetype='application/json')
        if not 'Content-Length' in self:
            self['Content-Length'] = len(self.content)


# TODO make tests for this "view interface" implementation
class ViewInterface(object):
    __name__ = 'renderer'
    url_pattern = None
    instance = None

    def __init__(self, func, url_pattern=None, instance=None, template=None, 
                 is_public=False, use_cache=False, cache_timeout=None,
				 use_siteskin=False, use_admin=False, use_geos=False):
        self.func = func
        self.url_pattern = url_pattern
        self.template = template
        self.instance = instance # provider_instance
        self.is_public = is_public
        self.use_cache = use_cache
        self.cache_timeout = cache_timeout
        self.use_siteskin = use_siteskin
        self.use_admin = use_admin
        self.use_geos = use_geos

    def __call__(self, request, *args, **kwargs):
        if self.use_geos:
            from spicy.core.service import api
            request.location_geos = api.register['map'].get_geos_from_request(
                request)

        if self.instance is not None:
            return self.func(self.instance, request, *args, **kwargs)
        return self.func(request, *args, **kwargs)

    def set_instance(self, instance):
        self.instance = instance
        

class ViewRendererToResponse(ViewInterface):
    def __call__(self, request, *args, **kwargs):

        if self.use_cache:
            cached_data = cache.get(make_cache_key(request))
            if cached_data:
                return HttpResponse(cached_data)

        output = super(
            ViewRendererToResponse, self).__call__(
            request, *args, **kwargs)

        if not isinstance(output, dict):
            if self.use_cache and isinstance(output, HttpResponse):
                cache.set(make_cache_key(request), output.content, 
                          self.cache_timeout or defaults.CACHE_TIMEOUT)

            return output
        
        response = render_to_response(
            self.template, output, 
            context_instance=RequestContext(request))

        if self.use_cache:
            cache.set(make_cache_key(request), response.content, 
                      self.cache_timeout or defaults.CACHE_TIMEOUT)
            
        response['Expires'] = 'now'
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'max-age=0'
        return response


class ViewMultiResponse(ViewInterface):
    def __call__(self, request, *args, **kwargs):
        if self.use_cache:
            cached_data = cache.get(make_cache_key(request))
            if cached_data:
                return HttpResponse(cached_data)

        output = super(
            ViewMultiResponse, self).__call__(request, *args, **kwargs)
        

        if not isinstance(output, dict):
            if self.use_cache and isinstance(output, HttpResponse):
                cache.set(make_cache_key(request), output.content, 
                      self.cache_timeout or defaults.CACHE_TIMEOUT)
            return output

        template = output.get('template', None)            
        if template is None:
            raise ValueError

        if self.use_siteskin:
            template = defaults.SITESKIN + '/' + template

        if self.use_admin:
            template = defaults.SITESKIN_ADMIN + '/' + template

        response = render_to_response(
            template, output, 
            context_instance=RequestContext(request))

        if self.use_cache:
            cache.set(make_cache_key(request), response.content, 
                      self.cache_timeout or defaults.CACHE_TIMEOUT)

        response['Expires'] = 'now'
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'max-age=0'
        return response


class JsonRenderer(ViewInterface):
    def __call__(self, request, *args, **kwargs):
        if self.use_cache:
            cached_data = cache.get(make_cache_key(request))
            if cached_data:
                return HttpResponse(cached_data)

        output = super(JsonRenderer, self).__call__(
            request, *args, **kwargs)

        if self.use_cache:
            cached_data = output
            if not isinstance(output, (dict, list)) and isinstance(output, HttpResponse):
                cached_data = output.content
            cache.set(make_cache_key(request), cached_data, 
                      self.cache_timeout or defaults.CACHE_TIMEOUT)
        
        if isinstance(output, (dict, list)):
            return JsonResponse(output)
        return output

def render_to(template, use_siteskin=False, use_admin=False, *args, **kwargs):
    """
    Parameters:
      - template: template name to use
      - use_siteskin: 
    """
    template = template
    if use_siteskin:
        template = defaults.SITESKIN + '/' + template

    elif use_admin:
        template = defaults.SITESKIN_ADMIN + '/' + template


    def wrapper(func):
        return ViewRendererToResponse(func, template=template, *args, **kwargs)
    return wrapper


def ajax_request(obj, *args, **kwargs):
    if callable(obj):
        return JsonRenderer(obj, *args, **kwargs)
    def wrapper(func):
        return JsonRenderer(func, url_pattern=obj, *args, **kwargs)
    return wrapper

def multi_view(*args, **kwargs):
    def wrapper(func):
        return ViewMultiResponse(func, *args, **kwargs)
    return wrapper
