# coding: utf-8
from django.conf import settings

#TODO: add logging

def is_settings_loaded():
    """Checks if django settings was initialized."""
    try:
        getattr(settings, 'DEBUG')

    except ImportError:
        return False

    return True


def get_default_value(setting_name):
    """Returns default setting value."""
    try:
        return getattr(settings, setting_name)

    except ImportError:
        return None
    except AttributeError:
        return None
