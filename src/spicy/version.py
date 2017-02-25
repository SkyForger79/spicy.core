version = (1, 2, 1)
__version__ = '.'.join(map(str, version))


# todo: move to utils?
def get_version():
    return __version__
