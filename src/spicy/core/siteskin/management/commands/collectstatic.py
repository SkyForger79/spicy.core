import os
import sys
from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic
from django.core.management.base import CommandError
from django.utils.datastructures import SortedDict
from spicy.core.siteskin import utils
from spicy.utils import load_module


class Command(collectstatic.Command):
    def collect(self):
        """
        Perform the bulk of the work of collectstatic.

        Split off from handle_noargs() to facilitate testing.
        """
        if self.symlink:
            if sys.platform == 'win32':
                raise CommandError("Symlinking is not supported by this "
                                   "platform (%s)." % sys.platform)
            if not self.local:
                raise CommandError("Can't symlink to a remote destination.")

        if self.clear:
            self.clear_dir('')

        if self.symlink:
            handler = self.link_file
        else:
            handler = self.copy_file

        found_files = SortedDict()
        for theme_path, theme in utils.get_siteskin_themes():
            for finder_path in settings.STATICFILES_FINDERS:
                finder = load_module(finder_path)(theme=theme)
                for path, storage in finder.list(self.ignore_patterns):
                    # Prefix the relative path if the source storage contains it
                    if getattr(storage, 'prefix', None):
                        prefixed_path = os.path.join(storage.prefix, path)
                    else:
                        prefixed_path = path

                    prefixed_path = os.path.join(theme, prefixed_path)

                    if prefixed_path not in found_files:
                        found_files[prefixed_path] = (storage, path)
                        handler(path, prefixed_path, storage)

        # Here we check if the storage backend has a post_process
        # method and pass it the list of modified files.
        if self.post_process and hasattr(self.storage, 'post_process'):
            processor = self.storage.post_process(found_files,
                                                  dry_run=self.dry_run)
            for original_path, processed_path, processed in processor:
                if processed:
                    self.log(u"Post-processed '%s' as '%s" %
                             (original_path, processed_path), level=1)
                    self.post_processed_files.append(original_path)
                else:
                    self.log(u"Skipped post-processing '%s'" % original_path)

        return {
            'modified': self.copied_files + self.symlinked_files,
            'unmodified': self.unmodified_files,
            'post_processed': self.post_processed_files,
        }
    
