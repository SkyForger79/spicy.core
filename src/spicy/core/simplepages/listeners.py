<<<<<<< local
import os


=======
>>>>>>> other
def reload_server(sender, instance, signal, **kwargs):
<<<<<<< local
    try:
        import uwsgi
        uwsgi.reload()
    except ImportError:
        try:
            os.utime(__file__, None)
        except:
            pass
=======
    from spicy.utils import reload_server
    reload_server()
>>>>>>> other
