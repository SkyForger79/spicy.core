# coding: utf-8
"""${APPNAME_CLASS} abstract models."""
from django.db import models


class ${APPNAME_CLASS}AbstractModel(models.Model):
    '''
    ${APPNAME_CLASS} docstring
    '''

    preview = models.TextField('${APPNAME} test field')

    class Meta:
        abstract = True
