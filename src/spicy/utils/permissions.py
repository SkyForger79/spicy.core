from functools import partial

def generate_random_password(length=10):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])


def perm(custom_model, prefix):
    app, model = custom_model.split('.', 1)
    return '{0}.{1}_{2}'.format(app, prefix, model.lower())


add_perm = partial(perm, prefix='add')
change_perm = partial(perm, prefix='change')
delete_perm = partial(perm, prefix='delete')


def app_perm(custom_model):
    return custom_model.split('.')[0]


__all__ = 'add_perm', 'change_perm', 'delete_perm', 'perm', 'app_perm'
