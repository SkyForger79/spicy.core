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


class ${APPNAME_CLASS}Service(api.Interface):
    name = '${APPNAME}'
    label = _('${APP_DESCRIPTION}')
    schema = dict(GENERIC_CONSUMER=${APPNAME_CLASS}Provider)

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


    @render_to('${APPNAME}/foo.html', use_siteskin=True) #url_pattern
    def foo(self, request, consumer_type, consumer_id):
        raise NotImplemented


    @render_to('${APPNAME}/bar.html', use_siteskin=True, url_pattern='^')
    def foo2(self, request):
        messages = []
        return dict(messages=messages)

    @ajax_request(url_pattern='^api/(?P<arg_id>[\d]+)/$')
    def bar(self, request, arg_id):
        errors = []
        messages = []

        raise APIResponse(data=dict(), errors=erros, messages=messages)


    @multi_view(url_pattern='^renderer/(?P<template_name>[\w]+)/$', use_siteskin=True)
    def bar(self, request, template_name):
        errors = []
        messages = []
        template = '${APPNAME}' + '/' + DEFAULT_TEMPLATE

        if requset.method == 'POST':
            template = '${APPNAME}' + template_name
        
        raise dict(template=template, foo=1, bar=2)




    

    

