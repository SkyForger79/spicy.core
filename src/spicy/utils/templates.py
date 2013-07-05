import os
from spicy.core.admin.conf import app_modules_register


def find_templates(base_dir, name_tuples=True):
    templates = []
    for app in app_modules_register.values():
        try:
            if name_tuples:
                templates.extend(
                    [(tmpl, tmpl) for tmpl in os.listdir(
                        os.path.join(
                            os.path.dirname(app.__file__), 'templates',
                            base_dir))])
            else:
                dir_name = os.path.join(
                    os.path.dirname(app.__file__), 'templates', base_dir)
                templates.extend(
                    [os.path.join(dir_name, template)
                     for template in os.listdir(dir_name)])
        except OSError:
            pass
    templates.sort()
    return templates
