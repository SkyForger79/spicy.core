from django.contrib.auth.models import Group, Permission, User
from django.core.cache import cache

from spicy.core.siteskin import defaults as sk_defaults

def get_permissions(user_obj, salt, perm_key):
    """
    Shared code for getting user and group info from cache or DB.
    
    @user_obj: django.contrib.auth.models.User instance.
    @salt: a string that distinguishes users from groups.
    @perm_key: key for permissions query.
    """
    if user_obj.is_anonymous():
        return set()

    local_attr = '_%s_perm_cache' % salt
    object_pk = 'Superuser' if user_obj.is_superuser else str(user_obj.pk)
    kwargs = {perm_key: user_obj}

    if not hasattr(user_obj, local_attr):
        cache_key = sk_defaults.CACHE_PREFIX + '|'.join(('Perm', salt.title(), object_pk))
        perms = cache.get(cache_key)
        if perms is None:
            # No cached perms found.
            if user_obj.is_superuser:
                # Superuser has all perms.
                queryset = Permission.objects.all().values_list(
                    'content_type__app_label', 'codename').order_by()
            else:
                # Get user perms.
                queryset = Permission.objects.filter(**kwargs).values_list(
                    'content_type__app_label', 'codename').order_by()

            perms = set([u"%s.%s" % perm for perm in queryset])
            
            # Set cache and local cache.
            cache.set(cache_key, perms)
                
        setattr(user_obj, local_attr, perms)
        
    return getattr(user_obj, local_attr)


def clear_permission_cache(salt, keys=None, superuser=False, user_obj=None):
    """
    Clear permissions cache. Either keys, superuser or user_obj should be passed.

    @salt: a string that distinguishes users from groups.
    @keys: a list of keys for objects to delete.
    @superuses: add superuser keys here?
    @user_obj: user object to clear.
    """
    if keys is None:
        keys = []
    else:
        keys = list(keys)        
        
    if user_obj:
        keys = [user_obj.pk]
        try:
            delattr(user_obj, '_%s_perm_cache' % salt)
        except AttributeError:
            # No local cache, not a problem.
            pass        
        
    if superuser:
        keys.append('Superuser')    

    to_clear = (sk_defaults.CACHE_PREFIX + '|'.join(('Perm', salt.title(), str(key))) for key in set(keys))
    cache.delete_many(to_clear)


####################
# Signal listeneres.
####################


def m2m_changed_permission(sender, instance, action, reverse, model, **kwargs):
    if not action in ('post_clear', 'post_add', 'post_remove'):
        return
    if model is Permission:
        if sender is User.user_permissions.through:
            clear_permission_cache('user', user_obj=instance)
        elif sender is Group.permissions.through:            
            clear_permission_cache(
                'group', instance.user_set.values_list('id', flat=True))
    elif model is User:
        clear_permission_cache(
            'user',
            instance.user_set.values_list('id', flat=True))
    elif model is Group:
        clear_permission_cache(
            'group',
            User.objects.filter(
                groups__in=instance.group_set.all()).values_list('id', flat=True))

def post_save_permission(sender, instance, created, **kwargs):
    post_delete_permission(sender, instance, **kwargs)

def post_delete_permission(sender, instance, **kwargs):
    # Clear superuser data.
    clear_permission_cache('user', [], True)
    clear_permission_cache('group', [], True)

    # Clear related users data.
    clear_permission_cache(
        'user', instance.user_set.values_list('id', flat=True),
        True)
    clear_permission_cache(
        'group',
        User.objects.filter(
            groups__in=instance.group_set.all()).values_list('id', flat=True),
        True)

def post_save_user(sender, instance, **kwargs):
    clear_permission_cache('user', [instance.pk])
    clear_permission_cache('group', [instance.pk])

post_delete_user = post_save_user

def post_save_group(instance, raw, **kwargs):
    if instance.pk:
        _pre_delete_group(instance, **kwargs)

def _pre_delete_group(instance, **kwargs):
    clear_permission_cache(
        'user',
        [perm[0] for perm in
         Permission.objects.filter(user__groups=instance).values_list('id')])
    clear_permission_cache(
        'group',
        [perm[0] for perm in
         Permission.objects.filter(group=instance).values_list('id')])
    

    
