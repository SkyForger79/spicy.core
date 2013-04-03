import sys
from . import defaults
from datetime import datetime as dt
from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.core.management.color import color_style


style = color_style()


def page_not_found(request, template_name='%s/404.html' % defaults.SITESKIN):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """

    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR(
            'handler404: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST,
                request.get_full_path())))

    t = loader.get_template(template_name)
    # You need to create a 404.html template.
    return http.HttpResponseNotFound(
        t.render(RequestContext(request, {'request_path': request.path})))


def forbidden(request, template_name='%s/403.html' % defaults.SITESKIN):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """

    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR(
            'handler403: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path())))

    t = loader.get_template(template_name)
    # You need to create a 403.html template.
    return http.HttpResponseNotFound(t.render(RequestContext(
        request, {'request_path': request.path})))


def server_error(request, template_name='%s/500.html' % defaults.SITESKIN):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR(
            'handler505: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path())))

    t = loader.get_template(template_name)
    # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(RequestContext(request)))


def render(request, template, **kwargs):
    """
    Example of universal rubric rendering
    """
    page = kwargs.pop('page', None)
    template = defaults.SITESKIN + '/' + ((
        'index/flatpages/' + (page.template_name or 'default.html'))
        if (page and page.content and page.content != 'autocreated')
        else template)
    return render_to_response(
        template,
        {'page_slug': kwargs.pop('page_slug', page.title if page else None)},
        context_instance=RequestContext(request), **kwargs)


class BlockElement:
    """
    For rubrics from dynamic content blocks
    """
    def __init__(self, block, prev):
        self.instance = block
        self.prev = prev
