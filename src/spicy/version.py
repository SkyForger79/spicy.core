version = (1, 5)
__version__ = '.'.join(map(str, version))


# todo: move to utils?
def get_version():
    return __version__
