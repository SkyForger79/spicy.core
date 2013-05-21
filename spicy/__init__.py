__import__('pkg_resources').declare_namespace(__name__)
VERSION = (1, 1)

def get_version():
    return '.'.join([str(x) for x in VERSION])
