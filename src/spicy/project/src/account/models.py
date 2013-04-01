# -*- coding: utf-8 -*-
from . import defaults
from django.db import models
from django.utils.translation import ugettext_lazy as _
from spicy.core.profile.models import ProfileBase


class Account(ProfileBase):
    class Meta(ProfileBase.Meta):
        db_table = 'auth_account'
        ordering = '-create_date',


