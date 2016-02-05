import os
from django.conf import settings
from spicy.core.admin.conf import app_modules_register


<<<<<<< local
def find_templates(base_dir, name_tuples=True, rel_path=False):
=======
def find_templates(
        base_dir, name_tuples=True, abs_path=None, rel_path=False,
        from_dict=None):
    if abs_path is None:
        abs_path = not name_tuples
>>>>>>> other
    templates = []

    from spicy.core.siteskin.utils import get_siteskin_settings
    try:
        paths = [
            os.path.join(
                get_siteskin_settings().theme, 'templates', base_dir)]
    except:
        # No themes configured.
        paths = []

    # load app tempaltes
    paths.extend([
        os.path.join(
            os.path.dirname(app.__file__), 'templates',
            base_dir)
        for app in app_modules_register.values()])

    for app in app_modules_register.values():
        backends_dir = os.path.join(os.path.dirname(app.__file__), 'backends')
        if os.path.exists(backends_dir):
            for backend in os.listdir(backends_dir):
                backend_dir = os.path.join(backends_dir, backend, 'templates')
                if os.path.exists(backend_dir):
                    paths.append(os.path.join(backend_dir, base_dir))

    paths.extend([
        os.path.join(template_dir, base_dir)
        for template_dir in settings.TEMPLATE_DIRS])

    for path in paths:
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
