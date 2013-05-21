# coding: utf-8
from django.conf import settings
from django import template
from django.template.loader_tags import BlockNode
from django.template import Template, Context, loader


register = template.Library()


@register.filter
def is_installed(value):
    """Checks if `app` in `INSTALLED_APPS`."""

    if value in settings.INSTALLED_APPS:
        return True
    return False
