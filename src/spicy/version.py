version = (1, 2)
__version__ = '.'.join(map(str, version))


# todo: move to utils?
def get_version():
    return __version__
