# coding: utf-8
"""${APPNAME} views."""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.core.service import api

from . import models


@render_to('${APPNAME}/test_template.html', use_siteskin=True)
def test_view(request, test_param):

    return dict(test_param=test_param)
