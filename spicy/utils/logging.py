# coding: utf-8
import time
import logging as log

# from django.conf import settings
from .printing import *


def timeit():
    """Counts function call time and logs it."""

    def decorator(func_to_decorate):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func_to_decorate(*args, **kwargs)
            elapsed = (time.time() - start)

            if settings.DEBUG is True:
                log.debug(print_info(
                    "timeit: {0} - {1} s.".format(
                        paint_text(func_to_decorate.__name__, 'green')

                    )))

            return result
        wrapper.__doc__ = func_to_decorate.__doc__
        wrapper.__name__ = func_to_decorate.__name__
        return wrapper
    return decorator
