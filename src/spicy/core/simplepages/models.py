from . import abs, defaults, listeners
from django.db.models.signals import post_save, post_delete


if defaults.USE_DEFAULT_SIMPLE_PAGE_MODEL:
    class DefaultSimplePage(abs.AbstractSimplePage):
        class Meta(abs.AbstractSimplePage.Meta):
            abstract = False


post_delete.connect(
    listeners.reload_server, sender=abs.AbstractSimplePage,
    dispatch_uid='post-save-simple-page')

post_save.connect(
    listeners.reload_server, sender=abs.AbstractSimplePage,
    dispatch_uid='post-save-simple-page')
