import os
from django.conf import settings
from spicy.core.admin.conf import app_modules_register


def find_templates(base_dir, name_tuples=True, rel_path=False):
    templates = []

    # load app tempaltes
    paths = [
        os.path.join(
            os.path.dirname(app.__file__), 'templates',
            base_dir)
        for app in app_modules_register.values()]

    paths.extend([
        os.path.join(template_dir, base_dir)
        for template_dir in settings.TEMPLATE_DIRS])

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


def mk_style(name):
    if name:
        return 'class="%s"' % name
    return ''
