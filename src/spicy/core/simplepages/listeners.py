import os


def reload_server(sender, instance, signal, **kwargs):
    try:
        import uwsgi
        uwsgi.reload()
    except ImportError:
        try:
            os.utime(__file__, None)
        except:
            pass
