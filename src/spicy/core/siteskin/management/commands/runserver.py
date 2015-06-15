import os
from django.conf import settings
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.staticfiles.management.commands import runserver
from spicy.core.siteskin import utils
from urlparse import urlparse


class Command(runserver.Command):
    def get_handler(self, *args, **options):
        """
        Returns the static files serving handler wrapping the default handler,
        if static files should be served. Otherwise just returns the default
        handler.

        """
        handler = super(Command, self).get_handler(*args, **options)
        use_static_handler = options.get('use_static_handler', True)
        insecure_serving = options.get('insecure_serving', False)
        if use_static_handler and (settings.DEBUG or insecure_serving):
            handler = StaticFilesHandler(handler)
            current_theme = utils.get_siteskin_settings().theme
            theme_name = os.path.basename(current_theme)
            handler.get_base_url = lambda: os.path.join(
                settings.STATIC_URL, theme_name, '')
            handler.base_url = urlparse(handler.get_base_url())
            return handler
        return handler
