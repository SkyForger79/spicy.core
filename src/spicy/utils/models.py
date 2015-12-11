# coding: utf-8
"""
Stuff utils for abstract models
"""
from django.db.models.loading import cache


def get_custom_model_class(custom_model_name):
    '''
    Returns class for abstract model

    Args:
        custom_model_name (str): Custom model name in format
        'app_name.CustomModel'
    '''
    return cache.get_model(*custom_model_name.split('.'))


def backend_factory(setting, class_name, delegate_methods=()):
    bases = ()
    backends = []
    from spicy.utils import load_module
    for backend in setting:
        backend_class = load_module(backend + '.' + class_name)
        if backend_class:
            bases += (backend_class, )
            backends.append(backend_class)

    def delegate_method(name):
        def _inner(self, *args, **kwargs):
            for backend in self.backends:
                try:
                    getattr(backend, name)(self, *args, **kwargs)
                except AttributeError:
                    pass

        return _inner

    attrs = dict(backends=backends, __module__=__name__)
    for method in delegate_methods:
        attrs[method] = delegate_method(method)

    class Meta:
        abstract = True
    attrs['Meta'] = Meta

    return type('DynamicBackend' + class_name, bases, attrs)


__all__ = 'get_custom_model_class', 'backend_factory'
