from . import abs, defaults

if defaults.USE_DEFAULT_SIMPLE_PAGE_MODEL:
    class DefaultSimplePage(abs.AbstractSimplePage):
        class Meta(abs.AbstractSimplePage.Meta):
            abstract = False
