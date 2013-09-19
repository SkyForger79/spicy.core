from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.db.models import Q, Model
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from django.db import transaction, connection

from django import forms

from django.template.loader import render_to_string

from spicy.core.profile.decorators import is_staff

from spicy.core.siteskin.decorators import ajax_request, render_to
from spicy.core.siteskin.common import NavigationFilter

from spicy.core.service import api


class TrashProvider(api.Provider):
    model = 'trash.models.TrashProviderModel'


class TrashService(api.Interface):
    name = 'trash'
    label = _('Trash provider service')

    provider_schema = dict(GENERIC_CONSUMER=TrashProvider)
