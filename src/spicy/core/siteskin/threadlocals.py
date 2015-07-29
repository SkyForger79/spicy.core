from threading import local

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, 'user', None)


def get_current_session():
    return getattr(_thread_locals, 'session', None)


def get_current_ip():
    return getattr(_thread_locals, 'ip', None)


def get_current_request():
    return getattr(_thread_locals, 'request', None)


class ThreadLocals(object):
    """Middleware that gets various objects from the
    request object and saves them in thread local storage."""
    def process_request(self, request):
        _thread_locals.request = request
        _thread_locals.user = getattr(request, 'user', None)
        _thread_locals.session = getattr(request, 'session', None)
        _thread_locals.ip = request.META.get('REMOTE_ADDR')
