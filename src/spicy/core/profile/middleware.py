from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth import load_backend, SESSION_KEY, BACKEND_SESSION_KEY

from . import defaults
from .models import AnonymousUser
from spicy.core.siteskin.defaults import SITESKIN


def get_user(request):
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()
    return user


class AuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The AuthMiddleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user(request)
        request.__class__.user = request._cached_user
        # if user is banned - cleaning his session
        if hasattr(request, 'user') and request.user.is_authenticated():
            user = request.user
            clear_cache = getattr(user, 'is_banned', False)
            if not clear_cache and user.is_staff:
                password_hash = request.session.get(
                    defaults.PASSWORD_HASH_KEY)
                if password_hash:
                    if password_hash != user.password:
                        clear_cache = True
                request.session[defaults.PASSWORD_HASH_KEY] = user.password

            if clear_cache:
                request.session.flush()
                request.user = AnonymousUser()
        return None

class SetRemoteAddrFromForwardedFor(object):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy that
    causes each request's REMOTE_ADDR to be set to 127.0.0.1.
    
    Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
    a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
    this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
    because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
    anybody can "fake" their IP address. Only use this when you can absolutely
    trust the value of HTTP_X_FORWARDED_FOR.

    To make it work with nginx, add this line to config in server settings:
    proxy_set_header X-Forwarded-For $remote_addr;
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
            # client's IP will be the first one.
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip
