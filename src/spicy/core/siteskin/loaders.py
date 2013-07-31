import os
from django.conf import settings
from django.template.loaders import filesystem, app_directories
from django.utils._os import safe_join


class SpicyLoaderMixin(object):
    def add_siteskin(self, template_name):
        template_names = [template_name]
        if (
                settings.SITESKIN and
                not template_name.startswith(settings.SITESKIN + '/')):
            template_names.append(
                os.path.join(settings.SITESKIN, template_name))
        return template_names


class FilesystemLoader(filesystem.Loader, SpicyLoaderMixin):
    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of
        the template dirs are excluded from the result set, for security
        reasons.
        """
        if not template_dirs:
            template_dirs = settings.TEMPLATE_DIRS
        template_names = self.add_siteskin(template_name)
        for template_name in template_names:
            for template_dir in template_dirs:
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


class AppLoader(app_directories.Loader, SpicyLoaderMixin):
    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of
        the template dirs are excluded from the result set, for security
        reasons.
        """
        if not template_dirs:
            template_dirs = app_directories.app_template_dirs
        template_names = self.add_siteskin(template_name)
        for template_name in template_names:
            for template_dir in template_dirs:
                try:
                    yield safe_join(template_dir, template_name)
                except UnicodeDecodeError:
                    # The template dir name was a bytestring that wasn't valid
                    # UTF-8.
                    raise
                except ValueError:
                    # The joined path was located outside of template_dir.
                    pass
