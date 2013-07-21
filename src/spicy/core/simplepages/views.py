# -*- coding: utf-8 -*-
from django import http
from django.template import RequestContext


def render_simplepage(request, page, **kwargs):
    """
    Example of universal rubric rendering
    """
    context = {'page_slug': page.title, 'page': page}
    context.update(**kwargs)
    
    return http.HttpResponse(page.get_template().render(RequestContext(request, context)))
