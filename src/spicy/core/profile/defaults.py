# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from spicy.utils.html import make_slug


ACCOUNT_ALLOWED_CHARS = 'abcdefghjkmnpqrstuvwxyz'\
    'ABCDEFGHJKLMNPQRSTUVWXYZ'\
    '23456789'
ACCOUNT_ALLOWED_CHARS = getattr(
    settings, 'ACCOUNT_ALLOWED_CHARS', ACCOUNT_ALLOWED_CHARS)
USERNAME_MAX_LENGTH = getattr(settings, 'USERNAME_MAX_LENGTH', 100)
SHA1_RE = getattr(settings, 'SHA1_RE', re.compile('^[a-f0-9]{40}$'))
ACCOUNT_ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 2)
CHECK_USER_AGREEMENT = getattr(settings, 'CHECK_USER_AGREEMENT', False)
REGISTRATION_ENABLED = getattr(settings, 'REGISTRATION_ENABLED', True)
MANUAL_ACTIVATION = getattr(settings, 'MANUAL_ACTIVATION', False)
NOTIFY_MANAGERS = getattr(settings, 'NOTIFY_MANAGERS', True)

USE_CAPTCHA = getattr(settings, 'USE_CAPTCHA', True)
# django.contrib.auth required settings

# XXX
settings.LOGIN_URL = getattr(settings, 'LOGIN_URL', '/signin/')
settings.LOGIN_REDIRECT_URL = '/'
settings.LOGOUT_URL = '/signout/'

# social-auth patch
settings.SOCIAL_AUTH_USERNAME_FIXER = make_slug

REASSOCIATION_TIMEOUT = getattr(settings, 'REASSOCIATION_TIMEOUT', 300)
# How many seconds will we let user to start reassociation with existing
# profile after authorization in a social network.

PASSWORD_HASH_KEY = '_PASSWORD_HASH'
BRUTEFORCE_CHECK = getattr(settings, 'BRUTEFORCE_CHECK', False)
BRUTEFORCE_SOFT_LIMIT = 5
BRUTEFORCE_SOFT_PERIOD = 300
BRUTEFORCE_HARD_LIMIT = 20
BRUTEFORCE_HARD_PERIOD = 3600
AUTH_ALLOW, AUTH_WARN, AUTH_DISALLOW = range(3)


ACCESS_CACHE_PREFIX = 'access-cache'
ACCESS_CACHE_PERIOD = 60  # Period for tracking doc access, in seconds.
ACCESS_RELOAD_PERIOD = 10  # Period for reloading doc access info in admin.

ACCESS_LEVEL = (
    (0, _('Public for web')),
    (1, _('Is visible for user of this web site domain only')),
    (2, _('Only my friends have access')),
    (3, _('Only for me. Access restricted.')),
    (4, _('Only prepaid access is avalable')),
)

DEFAULT_ACCESS_LEVEL = 0

DEFAULT_PROFILE_URL = getattr(
    settings, 'DEFAULT_PROFILE_URL', lambda u: u.get_absolute_url())

CUSTOM_USER_MODEL = getattr(
    settings, 'CUSTOM_USER_MODEL', 'profile.TestProfile')
CUSTOM_PERMISSION_PROVIDER_MODEL = getattr(
    settings, 'CUSTOM_PERMISSION_PROVIDER_MODEL',
    'profile.PermissionProviderModel')
CUSTOM_ROLE_MODEL = getattr(settings, 'CUSTOM_ROLE_MODEL', 'auth.Group')
RESTORE_PASSWORD_FORM = getattr(
    settings, 'RESTORE_PASSWORD_FORM',
    'spicy.core.profile.forms.RestorePasswordForm')

ADMIN_CREATE_PROFILE_FORM = getattr(
    settings, 'ADMIN_CREATE_PROFILE_FORM',
    'spicy.core.profile.forms.CreateProfileForm')
ADMIN_EDIT_PROFILE_FORM = getattr(
    settings, 'ADMIN_EDIT_PROFILE_FORM',
    'spicy.core.profile.forms.ProfileForm')

LOGIN_WARNING = getattr(settings, 'LOGIN_WARNING', False)

USE_HTML_EMAIL = getattr(settings, 'USE_HTML_EMAIL', False)
