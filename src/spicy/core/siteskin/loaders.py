import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.template.loaders import app_directories, filesystem
from django.utils._os import safe_join
from django.utils.datastructures import SortedDict
from django.contrib.staticfiles import finders, storage

from spicy.utils import print_error, print_text, print_success
from . import defaults, utils


class AppDirectoriesFinder(finders.AppDirectoriesFinder):

    def __init__(self, apps=None, *args, **kwargs):
        kwargs.pop('theme', None)
        super(AppDirectoriesFinder, self).__init__(apps, *args, **kwargs)


class ThemeStaticFinder(finders.FileSystemFinder):

    def __init__(self, apps=None, theme=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        # Maps dir paths to an appropriate storage instance
        self.storages = SortedDict()

        prefix = None
        
        root = safe_join(
            defaults.THEMES_PATH, theme or utils.get_siteskin_settings().theme,
            'static')

        if not os.path.isdir(root):
            print_error(
                'ERROR!\n'
                'Check THEMES_PATH and DEFAULT_THEME(CURRENT_THEME) settings vars\n'
                'Cannt lookup `static` and `templates` dirs inside\n'
                'Create siteskin theme path for static ``mkdir -p %s``\n'%root
            )

        
        if os.path.abspath(settings.STATIC_ROOT) == os.path.abspath(root):
            raise ImproperlyConfigured(
                "The STATICFILES_DIRS setting should not contain the "
                "STATIC_ROOT setting")
        if (prefix, root) not in self.locations:
            self.locations.append((prefix, root))

        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage


class ThemeTemplateLoader(filesystem.Loader):

    def get_template_sources(self, template_name, template_dirs=None):
        try:  # that is for easier debugging when db is down
            theme = utils.get_siteskin_settings().theme
        except Exception, e:
            print e
            if defaults.DEFAULT_THEME:
                theme = defaults.DEFAULT_THEME
            else:
                raise NotImplementedError(
                    'Set ABSOLUTE_THEME_PATH in settings.py')

        template_dir = safe_join(
            defaults.THEMES_PATH, theme,
            'templates')

        #if defaults.DEBUG_ERROR_PAGES
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


class BackendTemplateLoader(app_directories.Loader):

    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = app_directories.app_template_dirs
        for template_dir in template_dirs:
            app_dir = os.path.dirname(template_dir)

            backends_dir = os.path.join(app_dir, 'backends')
            if not os.path.exists(backends_dir):
                continue

            for backend in os.listdir(backends_dir):
                backend_dir = os.path.join(backends_dir, backend)
                if os.path.isdir(backend_dir):
                    try:
                        yield safe_join(
                            backend_dir, 'templates', template_name)
                    except UnicodeDecodeError:
                        # The template dir name was a bytestring that wasn't
                        # valid UTF-8.
                        raise
                    except ValueError:
                        # The joined path was located outside of template_dir.
                        pass


class ThemeStaticFilesStorage(storage.StaticFilesStorage):

    def __init__(self, *args, **kwargs):
        current_theme = utils.get_siteskin_settings().theme
        theme_name = os.path.basename(current_theme)
        super(ThemeStaticFilesStorage, self).__init__(
            location=settings.STATIC_ROOT,
            base_url=os.path.join(settings.STATIC_URL, theme_name, ''), *args,
            **kwargs)
