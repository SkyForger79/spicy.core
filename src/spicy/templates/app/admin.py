# coding: utf-8
"""${APPNAME_CLASS} admin."""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to
from spicy.core.service import api

from . import models


@is_staff
@render_to('${APPNAME}/main.html', use_admin=True)
def main(request):
    foo_text = _('foo text')

    return dict(
        bar=foo_text
    )
