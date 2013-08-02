from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from spicy import utils
from . import defaults


SimplePage = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


class Loader(BaseLoader):
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            simplepage = SimplePage.objects.get(template_name=template_name)
            return simplepage.get_template(), template_name
        except SimplePage.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
