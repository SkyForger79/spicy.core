from spicy.utils.models import get_custom_model_class
from . import defaults

Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)
