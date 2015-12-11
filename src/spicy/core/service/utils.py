from functools import wraps, update_wrapper

# Licence for MethodDecoratorAdaptor and auto_adapt_to_methods
#
# This code is taken from stackoverflow.com [1], the code being supplied by
# users 'Ants Aasma' [2] and 'Silent Ghost' [3] with modifications.  It is
# legally included here under the terms of the Creative Commons
# Attribution-Share Alike 2.5 Generic Licence [4]
#
# [1] http://stackoverflow.com/questions/1288498/using-the-same-decorator-with-arguments-with-functions-and-methods
# [2] http://stackoverflow.com/users/107366/ants-aasma
# [3] http://stackoverflow.com/users/12855/silentghost
# [4] http://creativecommons.org/licenses/by-sa/2.5/


class MethodDecoratorAdaptor(object):
    """
    Generic way of creating decorators that adapt to being
    used on methods
    """
    def __init__(self, decorator, func):
        update_wrapper(self, func)
        # NB: update the __dict__ first, *then* set
        # our own .func and .decorator, in case 'func' is actually
        # another MethodDecoratorAdaptor object, which has its
        # 'func' and 'decorator' attributes in its own __dict__
        self.decorator = decorator
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.decorator(self.func)(*args, **kwargs)

    def __get__(self, instance, owner):
        return self.decorator(self.func.__get__(instance, owner))


def auto_adapt_to_methods(decorator):
    """
    Takes a decorator function, and returns a decorator-like callable that can
    be used on methods as well as functions.
    """
    def adapt(func):
        return MethodDecoratorAdaptor(decorator, func)
    return wraps(decorator)(adapt)
