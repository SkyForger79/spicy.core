from . import defaults
from django.db.models import get_model


def get_concrete_profile():
    # TODO: @burus deprecated by get_custom_model_class?
    return get_model(*defaults.CUSTOM_USER_MODEL.split('.'))
