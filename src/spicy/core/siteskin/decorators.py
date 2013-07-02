# -*- coding: utf-8 -*- 
import inspect
import traceback
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.template import RequestContext, loader
from django.template.base import TemplateDoesNotExist, TemplateSyntaxError
from django.utils.translation import ugettext as _

from spicy.core.siteskin import cache, defaults
from spicy.utils import make_cache_key
from spicy.utils.printing import print_error, print_info, print_warning

from . import defaults, utils

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

AJAX_ACCESS_CONTROL_ALLOW_ORIGIN = getattr(settings, 'AJAX_ACCESS_CONTROL_ALLOW_ORIGIN', None)

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

        if AJAX_ACCESS_CONTROL_ALLOW_ORIGIN is not None:
            self['Access-Control-Allow-Origin'] = AJAX_ACCESS_CONTROL_ALLOW_ORIGIN;


# TODO make tests for this "view interface" implementation
class ViewInterface(object):
    __name__ = 'renderer'
    url_pattern = None
    instance = None
    template = None

    def __init__(self, func, url_pattern=None, instance=None, template=None,
                 is_public=False, use_cache=False,
                 cache_timeout=cache.default_timeout,
                 use_siteskin=False, use_admin=False, use_geos=False):
        self.func = func
        self.url_pattern = url_pattern
        self.instance = instance  # provider_instance

        self.is_public = is_public
        self.cache_timeout = cache_timeout

        self.use_cache = use_cache

        self.use_siteskin = use_siteskin
        self.use_admin = use_admin
        self.use_geos = use_geos

        self.module = inspect.getmodule(self.func)
        self.app_name = '.'.join(self.module.__name__.split('.')[:-1])

        if template is not None:
            self.template = self.get_template(template)

    def __call__(self, request, *args, **kwargs):
        # TODO: deprecated or use config here.
        if self.use_geos:
            # warn: cross import error
            from spicy.core.service import api
            request.location_geos = api.register['map'].get_geos_from_request(
                request)

        if self.instance is not None:
            return self.func(self.instance, request, *args, **kwargs)
        return self.func(request, *args, **kwargs)

    def update_context(self, context):
        """
        :param context: dictionary for template rendering.
        :type dict

        return context
        """
        if self.use_admin and self.module.__name__ != 'spicy.core.admin.conf':
            # warn: cross import error
            from spicy.core.admin.conf import admin_apps_register
            try:
                context.update(dict(app=admin_apps_register[self.app_name]))
            except KeyError:
                print_error('Can not load admin application class: {0}'.format(
                        self.module.__name__))

        return context

    def get_template(self, template_name):
        """Choose template for rendering.

        Uses self.use_admin and self.use_siteskin attributes.

        :param template_name: - Template name.
        """
        if self.use_siteskin:
            try:
                t = loader.find_template(template_name)
                return template_name
            except TemplateDoesNotExist:
                print_warning(
                    'Can not find template: {}'.format(template_name))
                return template_name
            except TemplateSyntaxError, e:
                return template_name
        elif self.app_name in template_name and self.use_admin:
            return template_name
        elif self.use_admin:
            app_template = self.app_name + '/admin/' + template_name
            try:
                t = loader.find_template(app_template)
                return app_template
            except TemplateDoesNotExist:
                template = 'spicy.core.admin/admin/app/' + template_name
                if defaults.SITESKIN_DEBUG:
                    code, line_num = inspect.getsourcelines(self.func)
                    print_info(
                        'Renderer uses admin template. App module: {0}. '
                        'Code line: {1}\n\n {2}\n'
                        'Template does not exist: {3}\n'
                        'Use common template: {4}\n'.format(
                            self.module.__name__, line_num,
                            ''.join(
                                code[:defaults.SITESKIN_DEBUG_CODE_LEN]),
                            app_template, template))
                return template
            except TemplateSyntaxError, e:
                return app_template

        return template_name

    def set_instance(self, instance):
        self.instance = instance


class ViewRendererToResponse(ViewInterface):
    def __call__(self, request, *args, **kwargs):

        if self.use_cache:
            cached_data = cache.get(make_cache_key(request))
            if cached_data:
                return HttpResponse(cached_data)

        output = super(
            ViewRendererToResponse, self).__call__(request, *args, **kwargs)

        if not isinstance(output, dict):
            if self.use_cache and isinstance(output, HttpResponse):
                cache.set(
                    make_cache_key(request), output.content,
                    self.cache_timeout)

            return output

        response = render_to_response(
            self.template, self.update_context(output),
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

        template = self.get_template(template)

        response = render_to_response(
            template, self.update_context(output),
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

        if not request.is_ajax() and not settings.DEBUG:
            return JsonResponse(
                APIResponseFail(
                    messages=[_('AJAX request required!')]).response()
            )

        if self.use_cache:
            # TODO: test. Return APIResponse?
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


def render_to(template, *args, **kwargs):
    """Render controller data to defined template

    See ``ViewInterface`` attributes for details.

    Common atrributes:

    :param template: template name to use
    :param use_siteskin: True|False
    :param use_admin: True|False
    :param use_cache: True|False

    """

    def wrapper(func):
        return ViewRendererToResponse(func, template=template, *args, **kwargs)
    return wrapper


def ajax_request(obj, *args, **kwargs):
    """Render controller and choose template inside controller algorithm.
    You controller must return a ``template`` variable to define used template.

    See ``ViewInterface`` attributes for details.

    Common atrributes:

    :param use_cache: True|False

    return: ``spicy.core.siteskin.decorators.JsonResponse`` instance
    """

    if callable(obj):
        return JsonRenderer(obj, *args, **kwargs)

    def wrapper(func):
        return JsonRenderer(func, url_pattern=obj, *args, **kwargs)
    return wrapper


def multi_view(*args, **kwargs):
    """Render controller and choose template inside controller algorithm.
    You controller must return a ``template`` variable to define used template.

    See ``ViewInterface`` attributes for details.

    Common atrributes:

    :param use_siteskin: True|False
    :param use_admin: True|False
    :param use_cache: True|False
    """
    def wrapper(func):
        return ViewMultiResponse(func, *args, **kwargs)
    return wrapper
