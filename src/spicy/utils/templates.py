import os
import traceback
from django.conf import settings
from spicy.core.admin.conf import app_modules_register
from spicy.utils.printing import print_error, print_text

def find_templates(base_dir, name_tuples=True):
    templates = []

    # load app tempaltes
    paths = [
        os.path.join(
            os.path.dirname(app.__file__), 'templates',
            base_dir)
        for app in app_modules_register.values()]

    for template_dir in settings.TEMPLATE_DIRS:
        paths.append(os.path.join(template_dir, base_dir))

    for path in paths:
        try:
            if name_tuples:
                templates.extend(
                    [(tmpl, tmpl) for tmpl in os.listdir(path)])
            else:
                templates.extend(
                    [os.path.join(path, template)
                     for template in os.listdir(path)])
        except OSError, e:
            #print_error(e)
            #print_text(traceback.format_exc())
            pass

    templates.sort()
    return templates
