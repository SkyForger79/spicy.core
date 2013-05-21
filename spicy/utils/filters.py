from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

# OBJECTS_PER_PAGE = getattr(settings, 'OBJECTS_PER_PAGE', 50)
# DEFAULT_FILTERS = getattr(settings, 'DEFAULT_FILTERS',
#                           [('search_text', ''),])

#TODO: refactor to defaults
from spicy.utils.configuration import is_settings_loaded, get_default_value

OBJECTS_PER_PAGE = 50
DEFAULT_FILTERS = [('search_text', ''),]


if is_settings_loaded():
    OBJECTS_PER_PAGE = get_default_value('OBJECTS_PER_PAGE')
    DEFAULT_FILTERS = get_default_value('DEFAULT_FILTERS')
else:
    pass


class NavigationFilter:
    def __init__(self, request, accepting_filters=DEFAULT_FILTERS,
                 default_order=None, force_filter=None):
        self.request = request
        self.querydict = request.GET

        self.order = None

        self.filter = ''

        if 'filter' in request.GET:
            self.filter = request.GET['filter']
        if force_filter:
            self.filter = force_filter

        for filter, default in accepting_filters:
            setattr(self, filter, request.GET.get(filter, default))

        self.page = request.GET.get('page', 1)

        self.field = request.GET.get('field', default_order)
        fields = self.field.split(' ') if self.field else None
        self.order_q = request.GET.get('order', 'asc')
        if fields and self.order_q:
            direction = '-' if self.order_q.lower() == 'desc' else ''
            self.order = [direction + field for field in fields]

    def get_queryset_with_paginator(
        self, model, base_url=None, search_query=None,
        obj_per_page=OBJECTS_PER_PAGE, manager='objects',
        result_manager='objects', distinct=False):

        base_url = base_url or self.request.path

        model_manager = getattr(model, manager)
        model_qset = model_manager.values_list('id', flat=True)
        
        # XXX: check usage
        if type(search_query) is dict:
            queryset = model_qset.filter(**search_query)

        elif type(search_query) is tuple:
            queryset = model_qset.filter(*search_query[0], **search_query[1])

        elif callable(search_query): # XXX
            queryset = search_query(model_qset)

        elif search_query is not None:
            queryset = model_qset.filter(search_query)

        else:
            queryset = model_qset.all()

        if self.order:
            queryset = queryset.order_by(*self.order)

        if distinct:
            queryset = queryset.distinct()

        paginator = Paginator(
            queryset, obj_per_page)
        try:

            page = paginator.page(self.page)
        except InvalidPage:
            raise Http404(unicode(_('Page %s does not exist.' % self.page)))
            # Django that can't throw exceptions other than 404.

        result_qset = getattr(
            model, result_manager).filter(
            id__in=tuple(page.object_list))
        if self.order:
            result_qset = result_qset.order_by(*self.order) # 1082

        # XXX
        page.object_list = result_qset

        paginator.current_page = page
        paginator.current_object_list = result_qset

        paginator.base_url = base_url

        return paginator

