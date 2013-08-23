from . import defaults
from django import http
from django.template import RequestContext
from spicy.utils import get_custom_model_class


SimplePage = get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


def render_simplepage(request, page, **kwargs):
    """
    Example of universal rubric rendering
    """
    if isinstance(page, basestring):
        page = SimplePage.objects.get(url=page)
    context = {'page_slug': page.title, 'page': page}
    context.update(**kwargs)
    return http.HttpResponse(
        page.get_template().render(RequestContext(request, context)))
