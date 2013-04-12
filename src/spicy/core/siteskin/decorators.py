# -*- coding: utf-8 -*- 
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _

from spicy.core.siteskin import cache, defaults
from spicy.utils import make_cache_key
from spicy.utils.printing import print_error

from . import defaults

class APIResponse(object):
    """Класс представляет объек ответа API функций.
    
    :param version: версия API 
    :type version: str
    :param code: код результата, может быть либо ``success``, либо ``error``. По умолчанию: ``JSON_API_STATUS_CODE_SUCCESS``
    :type code: str
    :param messages: список сообщений, описывающие результат. По умолчанию: None
    :type messages: list
    :param errors: словарь с ошибками. По умолчанию: None
    :type errors: dict
    :param data: словарь с данными, представляющими результат работы API функции. По умолчанию: None
    :type data: dict
    """
    
    version = defaults.AJAX_API_VERSION
    code = defaults.AJAX_API_STATUS_CODE_SUCCESS
    messages = None
    errors = None
    data = None
    
    def __init__(self, code=defaults.AJAX_API_STATUS_CODE_SUCCESS, messages=None, data=None, errors=None):
        """Инициализирует объект :class:`APIResponse`

        :param code: код результата, может быть либо ``success``, либо ``error``
        :type code: str
        :param messages: список сообщений, описывающие результат
        :type message: list
        :param errors: словарь с ошибками. По умолчанию: None
        :type errors: dict
        :param data: словарь с данными, представляющими результат работы API функции
        :type data: dict
        """
        self.code = code
        self.messages = messages
        self.data = data
        self.errors = errors

    def response(self):
        """Возвращает словарь с данными для преобразования в JSON и ответа клиентскому приложению.

        :return: version, code, message, data, errors
        :rtype: dict
        """
        return dict(
            version=self.version,
            code=self.code,
            messages=self.messages,
            errors=self.errors,
            data=self.data,
        )


class APIResponseFail(APIResponse):
    def __init__(self, messages=None, data=None, errors=None):
        super(APIResponseFail, self).__init__(
            code=defaults.AJAX_API_STATUS_CODE_ERROR,
            messages=messages,
            data=data,
            errors=errors,
        )


class JsonResponse(HttpResponse):
    """
    HttpResponse descendant, which return response with ``application/json``
    mimetype.
    """
    def __init__(self, data):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(data, cls=DjangoJSONEncoder),
            mimetype='application/json')
        if not 'Content-Length' in self:
            self['Content-Length'] = len(self.content)


# TODO make tests for this "view interface" implementation
class ViewInterface(object):
    __name__ = 'renderer'
    url_pattern = None
    instance = None

    def __init__(self, func, url_pattern=None, instance=None, template=None,
                 is_public=False, use_cache=False,
                 cache_timeout=cache.default_timeout,
                 use_siteskin=False, use_admin=False, use_geos=False):
        self.func = func
        self.url_pattern = url_pattern
        self.template = template
        self.instance = instance  # provider_instance
        self.is_public = is_public
        self.cache_timeout = cache_timeout
        self.use_cache = use_cache
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
                cache.set(
                    make_cache_key(request), output.content,
                    self.cache_timeout)

            return output

        response = render_to_response(
            self.template, output,
            context_instance=RequestContext(request))

        if self.use_cache:
            cache.set(
                make_cache_key(request), response.content, self.cache_timeout)
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
                cache.set(
                    make_cache_key(request), output.content,
                    self.cache_timeout)
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
            cache.set(
                make_cache_key(request), response.content, self.cache_timeout)

        response['Expires'] = 'now'
        response['Pragma'] = 'no-cache'
        response['Cache-Control'] = 'max-age=0'
        return response


class JsonRenderer(ViewInterface):
    def __call__(self, request, *args, **kwargs):
        if not request.is_ajax():
            return JsonResponse(
                APIResponseFail(messages=[_('AJAX request required!'),]).response()
            )

        if self.use_cache:
            cached_data = cache.get(make_cache_key(request))
            if cached_data:
                return HttpResponse(cached_data)

        output = super(JsonRenderer, self).__call__(
            request, *args, **kwargs)

        if self.use_cache:
            cached_data = output
            if not isinstance(output, (dict, list)) and isinstance(
                output, HttpResponse):
                cached_data = output.content
            cache.set(
                make_cache_key(request), cached_data, self.cache_timeout)

        if isinstance(output, (dict, list)):
            return JsonResponse(output)
        elif isinstance(output, APIResponse):
            return JsonResponse(output.response())
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
