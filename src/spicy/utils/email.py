__all__ = 'process_email',


def process_email(text, sender, kind):
    from django.conf import settings
    name = ':'.join((sender.__class__.__name__.lower(), kind))
    from spicy.utils import load_module
    for processor_path in getattr(
            settings, 'EMAIL_PROCESSORS', {}).get(name, ()):
        processor = load_module(processor_path)
        new_text = processor.get_text(text, sender=sender, kind=kind)
        if new_text:
            text = new_text

    return text
