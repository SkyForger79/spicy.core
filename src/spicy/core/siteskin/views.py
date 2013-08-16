from datetime import datetime as dt
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from spicy.utils.printing import print_error
from . import defaults


def page_not_found(request, template_name='404.html'):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error('handler404: %s %s %s %s\n' % (
            dt.now(), request.GET, request.POST, request.get_full_path()))

    t = loader.get_template(template_name)
    # You need to create a 404.html template.
    return http.HttpResponseNotFound(
        t.render(RequestContext(request, {'request_path': request.path})))


def forbidden(request, template_name='403.html'):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """

    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler403: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    t = loader.get_template(template_name)
    # You need to create a 403.html template.
    return http.HttpResponseNotFound(t.render(RequestContext(
        request, {'request_path': request.path})))


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler505: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    t = loader.get_template(template_name)
    # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(RequestContext(request)))


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
