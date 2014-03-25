from . import defaults
from django import http
from django.template import RequestContext
from spicy.utils import get_custom_model_class
from django.shortcuts import get_object_or_404


SimplePage = get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


def render_simplepage(request, page, **kwargs):
    """
    Example of universal rubric rendering
    """
    if isinstance(page, basestring):
        page = SimplePage.objects.get(url=page)
    if page.is_active and not request.user.is_staff:
        page = get_object_or_404(SimplePage, url='/errors/404/')
    context = {'page_slug': page.title, 'page': page}
    context.update(**kwargs)
    content_type = 'text/plain' if page.url.endswith('.txt') else 'text/html'
    return http.HttpResponse(
        page.get_template().render(RequestContext(request, context)),
        content_type=content_type)
