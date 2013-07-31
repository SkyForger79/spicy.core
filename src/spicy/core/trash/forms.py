from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.db import transaction

from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory

from django.contrib.sites.models import Site
