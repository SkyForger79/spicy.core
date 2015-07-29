from django.conf import settings
from django.db import models
from spicy.utils import get_custom_model_class


class CustomSettings(models.Model):
    class Meta:
        abstract = True

# TODO
def get_settings_from_db(model_name, field):
    return get_custom_model_class(model_name).objects.get(site__id=SITE_ID)
