from . import defaults
from django.db.models import get_model


def get_concrete_profile():
    return get_model(*defaults.CUSTOM_USER_MODEL.split('.'))
