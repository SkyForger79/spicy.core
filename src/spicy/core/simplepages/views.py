# -*- coding: utf-8 -*-
from django import http
from django.template import RequestContext, Template


def render_simplepage(request, page, **kwargs):
    """
    Example of universal rubric rendering
    """
    template = Template(page.content)
    context = {'page_slug': page.title, 'page': page}
    context.update(**kwargs)
    return http.HttpResponse(template.render(RequestContext(request, context)))
