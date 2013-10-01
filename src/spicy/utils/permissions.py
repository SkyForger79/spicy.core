from functools import partial


def perm(custom_model, prefix):
    app, model = custom_model.split('.', 1)
    return '{0}.{1}_{2}'.format(app, prefix, model.lower())


add_perm = partial(perm, prefix='add')
change_perm = partial(perm, prefix='change')
delete_perm = partial(perm, prefix='delete')

__all__ = 'add_perm', 'change_perm', 'delete_perm', 'perm'
