# coding: utf-8
"""${APPNAME_CLASS} models."""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from . import defaults
from . import abs


class ${APPNAME_CLASS}Model(abs.${APPNAME_CLASS}AbstractModel):

    field2 = models.TextField(_('foo baz'))
