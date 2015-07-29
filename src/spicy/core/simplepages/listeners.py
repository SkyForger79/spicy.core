def reload_server(sender, instance, signal, **kwargs):
    from spicy.utils import reload_server
    reload_server()
