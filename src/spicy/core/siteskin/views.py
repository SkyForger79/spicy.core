from datetime import datetime as dt
from django.shortcuts import render_to_response
from django.template import RequestContext
from spicy.core.simplepages.views import render_simplepage
from spicy.utils.printing import print_error
from . import defaults
from spicy.core.simplepages import defaults as sp_defaults
from spicy.utils.models import get_custom_model_class
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django import http

SimplePage = get_custom_model_class(sp_defaults.SIMPLE_PAGE_MODEL)
SiteskinModel = get_custom_model_class(defaults.SITESKIN_SETTINGS_MODEL)

def page_not_found(request):
    """
    Default 404 handler.
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error('handler404: %s %s %s %s\n' % (
            dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/404/')
    response.status_code = 404
    return response


def forbidden(request):
    """
    Default 403 handler.
    """

    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler403: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/403/')
    response.status_code = 403
    return response


def server_error(request):
    """
    500 error handler.
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler505: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/500/')
    response.status_code = 500
    return response


def render(
        request, template_name, context_intstance=None, mimetype=None,
        **kwargs):
    """
    Example of universal rubric rendering
    """
    # XXX mimetype is renamed to content_type in django 1.5!
    try:
        home_page = SiteskinModel.objects.get(site=Site.objects.get_current())
    except SiteskinModel.DoesNotExist:
        home_page = None
    try:
        page = SimplePage.objects.get(pk=home_page.home_page.id)
    except AttributeError:
        page = get_object_or_404(SimplePage, url='/index/')
    except SimplePage.DoesNotExist:
        page = get_object_or_404(SimplePage, url='/index/')
    context = {'page_slug': page.title, 'page': page}
    context.update(**kwargs)
    content_type = 'text/plain' if page.url.endswith('.txt') else 'text/html'
    return http.HttpResponse(
       page.get_template().render(RequestContext(request, context)),
       content_type=content_type)

