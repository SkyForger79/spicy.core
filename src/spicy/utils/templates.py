import os
from django.conf import settings
from spicy.core.admin.conf import app_modules_register


def find_templates(
        base_dir, name_tuples=True, abs_path=None, rel_path=False,
        from_dict=None):
    if abs_path is None:
        abs_path = not name_tuples
    templates = []

    # load app tempaltes
    path = [
        os.path.join(
            os.path.dirname(app.__file__), 'templates',
            base_dir)
        for app in app_modules_register.values()]

    path.extend([
        os.path.join(template_dir, base_dir)
        for template_dir in settings.TEMPLATE_DIRS])

    for path in path:
        try:
            if name_tuples:
                templates.extend(
                    [(
                        os.path.join(path, template) if abs_path else (
                            os.path.join(
                                base_dir, template) if rel_path else template),
                        from_dict.get(
                            template, template) if from_dict else template)
                     for template in os.listdir(path)])
            else:
                templates.extend(
                    [os.path.join(path, template) if abs_path else (
                        os.path.join(base_dir, template) if rel_path else path)
                     for template in os.listdir(path)])
        except OSError:
            pass

    templates.sort()
    return templates


def mk_style(name):
    if name:
        return 'class="%s"' % name
    return ''
