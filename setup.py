from importlib import import_module
from setuptools import setup, find_packages
import pkg_resources

spicy_pkg = import_module('src.spicy')
version = import_module('src.spicy.version').__version__

long_description = """spicy core package"""

pkg_resources.declare_namespace('spicy')


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

    packages=find_packages('src'),
    package_dir={'': 'src',},

    include_package_data=True,
    zip_safe=False,
    long_description=long_description(),

    install_requires=[
        'Django==1.4.11',
        'Fabric==1.6',
        'Sphinx==1.2b1',
        'numpydoc==0.4',
        'raven==3.2.1',
        'python-memcached==1.48',
        'uwsgi',

        # spicy.scripts.py: deploy
<<<<<<< local
        'configparser==3.3.0.post2',
=======
        # 'configparser==3.3.0r2',
        'configparser',
>>>>>>> other
        'Jinja2==2.6',

        # ?? siteskin deps.
        'pytils==0.2.3',
        'pytz==2013b',
        'html5lib==0.95',
        'python-redmine==0.8.1',

        #'django-simple-captcha', # spicy.core.profile
        #'django-social-auth==0.6.1',# spicy.core.profile

        # debug deps.
        # 'logutils', #TODO: version?
        'numpydoc',
        'django-nose',
        'django-debug-toolbar',
        'django-devserver',
        'django-extensions',
        'django-autocomplete-light==2.0.0a15',
        # For LDAP auth backend
        'django-auth-ldap==1.2.6',

        'xlrd',
        'xlwt'
    ],

    dependency_links=[
        # Spicy db settings
        # Warning! This package patches Django, see readme at https://code.spicycms.com/spicy.dbsettings
        'hg+https://code.spicycms.com/spicy.dbsettings#egg=spicy.dbsettings',

        # 'svn+http://django-simple-captcha.googlecode.com/svn/trunk@54#egg=django-captcha',
        # 'git+https://github.com/krvss/django-social-auth.git#egg=django-social-auth-0.7.13.dev',
    ],
    entry_points={
        'console_scripts': [
            'spicy = spicy.script:handle_command_line',
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Development Status :: 1.1',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
