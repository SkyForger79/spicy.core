from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.context_processors import PermWrapper
from django.utils.functional import lazy, SimpleLazyObject

from . import defaults
from .models import AnonymousUser

def auth(request):
    def get_user():
        return request.user if hasattr(request, 'user') else AnonymousUser()

    return {
        'next_url': request.GET.get(REDIRECT_FIELD_NAME, ''),
        'ACCESS_RELOAD_PERIOD': defaults.ACCESS_RELOAD_PERIOD,
        'MANUAL_ACTIVATION': defaults.MANUAL_ACTIVATION,
        
        #'user': SimpleLazyObject(get_user), use request.user ONLY !!!!
        'messages': messages.get_messages(request),
        'perms': lazy(lambda: PermWrapper(get_user()), PermWrapper)(),
        'auth_form': SimpleLazyObject(AuthenticationForm),
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
    }
