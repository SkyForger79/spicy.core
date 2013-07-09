import os
from django.conf import settings
from spicy.core.admin.conf import app_modules_register


def find_templates(base_dir, name_tuples=True):
    templates = []
    paths = [
        os.path.join(
            os.path.dirname(app.__file__), 'templates',
            base_dir)
        for app in app_modules_register.values()]
    paths.extend(settings.TEMPLATE_DIRS)
    for path in paths:
        try:
            if name_tuples:
                templates.extend(
                    [(tmpl, tmpl) for tmpl in os.listdir(path)])
            else:
                templates.extend(
                    [os.path.join(path, template)
                     for template in os.listdir(path)])
        except OSError:
            pass
    templates.sort()
    return templates
