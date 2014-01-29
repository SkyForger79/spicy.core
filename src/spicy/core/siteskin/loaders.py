import os
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.template.loaders import filesystem
from django.utils._os import safe_join
from django.utils.datastructures import SortedDict
from django.contrib.staticfiles import finders

from . import defaults, utils


class ThemeStaticFinder(finders.FileSystemFinder):
    def __init__(self, apps=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = SortedDict()

        prefix = None
        root = safe_join(
            defaults.THEMES_PATH, utils.get_siteskin_settings().theme,
            'static')

        if os.path.abspath(settings.STATIC_ROOT) == os.path.abspath(root):
            raise ImproperlyConfigured(
                "The STATICFILES_DIRS setting should "
                "not contain the STATIC_ROOT setting")
        if (prefix, root) not in self.locations:
            self.locations.append((prefix, root))

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage


class ThemeTemplateLoader(filesystem.Loader):
    # TODO
    # load tempalte_dir from Database in the __init__

    def get_template_sources(self, template_name, template_dirs=None):
        #template_dir = safe_join(
        #    defaults.THEMES_PATH, admin_defaults.DEFAULT_THEME)
        #if admin_settings.current_theme:
        template_dir = safe_join(
            defaults.THEMES_PATH, utils.get_siteskin_settings().theme,
            'templates')
        
        try:
            yield safe_join(template_dir, template_name)
        except UnicodeDecodeError:
            # The template dir name was a bytestring that wasn't
            # valid UTF-8.
            raise
        except ValueError:
            # The joined path was located outside of this particular
            # template_dir (it might be inside another one, so this
            # isn't fatal).
            pass
        

