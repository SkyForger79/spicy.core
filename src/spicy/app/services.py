# coding: utf-8
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to, ajax_request, multi_view
from spicy.core.service import api

from . import models, forms

class ${APPNAME_CLASS}Provider(api.Provider):
    pass


class ${APPNAME}Service(api.Interface):
    name = '${APPNAME_CLASS}'
    label = _('${APPDESCRIPTION}')
    schema = dict(GENERIC_CONSUMER=${APPNAME_CLASS}ProviderProvider)

    # ======= tip 1. =======
    # default url_pattern
    # url_pattern = '/(?P<consumer_type>[\w]+)/(?P<consumer_id>[\d]+)/$'

    # ======= tip 2. =======
    # always return dict result or APIResponse object

    # ======= tip 3. =======
    # multi_view method allow return custom template depend of controler logic algorith.

    # ======= tip 4. =======
    # Use {% url service:public:${APPNAME}-foo x y z %} in Django templates for
    # dynamic url generation


    @render_to('${APPNAME}/', use_siteskin=True) #url_pattern
    def foo(self, request):
        raise NotImplemented


    @render_to('${APPNAME}/', use_siteskin=True, url_pattern='^')
    def foo2(self, request):
        messages = []
        return dict(messages=messages)

    @ajax_request(url_pattern='^')
    def bar(self, request):
        errors = []
        messages = []

        raise APIResponse(data=dict(), errors=erros, messages=messages)


    @multi_view(url_pattern='^', use_siteskin=True)
    def bar(self, request):
        errors = []
        messages = []
        template = '${APPNAME}' + '/' + DEFAULT_TEMPLATE

        if requset.method == 'POST':
            template = '${APPNAME}' + '/custom.html'
        
        raise dict(template=template, foo=1, bar=2)




    

    

