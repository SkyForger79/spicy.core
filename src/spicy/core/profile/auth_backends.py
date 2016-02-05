from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model

from django_auth_ldap.backend import LDAPBackend

from spicy.core.profile import cache, defaults

#from social_auth.backends import OpenIDBackend, OpenIdAuth
#from social_auth.backends.contrib.yandex import YandexBackend, YandexAuth
#from social_auth.backends.contrib.livejournal import LiveJournalBackend, LiveJournalAuth


class CustomUserModelBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        user_model = self.get_user_model()
        if '@' in username:
            kwargs = {'email__iexact': username}
        else:
            kwargs = {'username__iexact': username}
        kwargs['is_banned'] = False

        try:
            user = user_model.objects.get(**kwargs)
            current_site = Site.objects.get_current()
            
            # TODO make specific exception for site and passwd/username

            if (user.check_password(password) 
                #and user.sites.filter(pk=current_site.pk).exists()
                ):
                return user

        except user_model.DoesNotExist:
            return None

    def get_user(self, user_id):
        user_model = self.get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

    def get_user_model(self):
        user_model = None
        if not hasattr(self, '_user_model'):
            app, model = defaults.CUSTOM_USER_MODEL.split('.', 1)

            user_model = get_model(app, model)
            if not user_model:
                raise ImproperlyConfigured(
                    'Could not get custom user model',
                    defaults.CUSTOM_USER_MODEL)
            self._user_model = user_model
        return self._user_model

    def get_group_permissions(self, user_obj, obj=None):
        return cache.get_permissions(user_obj, 'group', 'group__user')
    
    def get_all_permissions(self, user_obj, obj=None):
        perms = cache.get_permissions(user_obj, 'user', 'user')
        perms.update(cache.get_permissions(user_obj, 'group', 'group__user'))
        return perms


class CustomUserModelLDAPBackend(LDAPBackend):
    """
    For using as LDAP backend in AUTHENTICATION_BACKENDS setting.

    e.g.
    AUTHENTICATION_BACKENDS = ('spicy.core.profile.auth_backends.CustomUserModelLDAPBackend',
                               'spicy.core.profile.auth_backends.CustomUserModelBackend')
    """
    def get_user_model(self):
        """ Override base method to use custom user model rather than User model """
        app, model = defaults.CUSTOM_USER_MODEL.split('.', 1)
        user_model = get_model(app, model)
        if not user_model:
            raise ImproperlyConfigured(
                'Could not get custom user model',
                defaults.CUSTOM_USER_MODEL)
        return user_model

    def get_or_create_user(self, username, ldap_user):
        """ Override for mark profile as LDAP user """
        profile, created = super(CustomUserModelLDAPBackend, self).get_or_create_user(username, ldap_user)
        # Mark profile as LDAP user
        if created:
            profile.is_ldap_user = True
            profile.save()
        return profile, created


"""
class NoEmailMonkeyPatch(object):
    def get_user_details(self, response):
        details = self.__class__.__bases__[1].get_user_details(self, response)
        details['email'] = ''
        return details

        
class MonkeyPatchedOpenIDBackend(NoEmailMonkeyPatch, OpenIDBackend):
    pass

OpenIDBackend.AUTH_BACKEND = MonkeyPatchedOpenIDBackend


class MonkeyPatchedYandexBackend(NoEmailMonkeyPatch, YandexBackend):
    pass

YandexBackend.AUTH_BACKEND = MonkeyPatchedYandexBackend

class MonkeyPatchedLiveJournalBackend(NoEmailMonkeyPatch, LiveJournalBackend):
    pass

LiveJournalBackend.AUTH_BACKEND = MonkeyPatchedLiveJournalBackend


BACKENDS = {
    'yandex': YandexAuth,
    'openid': OpenIdAuth,
    'livejournal': LiveJournalAuth
}
"""
