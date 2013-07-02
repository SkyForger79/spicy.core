# -*- coding: utf-8 -*-
from django.shortcuts import render


def render_simplepage(request, page, **kwargs):
    """
    Example of universal rubric rendering
    """
    template = page.template_name

    return render(
        request, template, {'page_slug': page.title}, **kwargs)
