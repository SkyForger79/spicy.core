from datetime import datetime as dt
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from spicy.core.simplepages.views import render_simplepage
from spicy.utils.printing import print_error
from . import defaults


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
    context = RequestContext(request)
    return render_to_response(
        template_name, kwargs, context_instance=RequestContext(request),
        mimetype=mimetype)
