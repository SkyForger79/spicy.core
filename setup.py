from importlib import import_module
from setuptools import setup, find_packages

spicy_pkg = import_module('src.spicy')
version = unicode(spicy_pkg.__version__)
long_description = """spicy core package"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open('README.rst').read()
    except IOError:
        return long_description


setup(
    name='spicy',
    version=version,

    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description='spicy',
    license='BSD',
    keywords='django, cms',
    url='', # TODO: define an url

    packages=packages,
    package_data=package_data,
    
    packages=find_packages('src'),
    package_dir={'': 'src',},
    include_package_data=True,
    zip_safe=False,
    long_description=long_description(),

    install_requires=[
        'Django==1.4.3',
        'Fabric==1.6',
        'Sphinx==1.2b1',
        'numpydoc==0.4',
        'raven==3.2.1',
        'python-memcached==1.48',
        
        # spicy.scripts.py: deploy
        'configparser==3.3.0r2',
        'Jinja2==2.6',

        # ?? siteskin deps.
        'pytils==0.2.3',
        'pytz',
        'html5lib==0.95',

        #'django-crispy-forms==1.2.6', ??? for admin forms customization. Think about it later.
        #'django-simple-captcha', # spicy.core.profile
        #'django-social-auth==0.6.1',# spicy.core.profile

        # debug deps.
        # 'logutils', #TODO: version?
        'pycallgraph',
        'numpydoc',
        'django-nose',
        'django-debug-toolbar',
        'django-devserver',
        'django-extensions',
    ],

    entry_points={
        'console_scripts': [
            'spicy = spicy.script:handle_command_line',
        ],
    },
)
