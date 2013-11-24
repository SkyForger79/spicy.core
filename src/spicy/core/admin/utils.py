from django.conf import settings
from spicy.utils.models import get_custom_model_class
from . import defaults

def get_admin_settings():
    # TODO make cache wrapper
    SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)
    instance, _ = SettingsModel.objects.get_or_create(site_id=settings.SITE_ID)

    return instance
