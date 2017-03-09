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
        return open('README.md').read()
    except IOError:
        return long_description


setup(
    name='spicy',
    version='1.2.1',

    author='Burtsev Alexander',
    author_email='ab@bramabrama.com',
    description='SpicyCMS core modules',
    license='BSD',
    keywords='django, cms',
    url='http://spicycms.com', # TODO: define an url

    packages=find_packages('src'),
    package_dir={'': 'src',},

    include_package_data=True,
    zip_safe=False,
    long_description=long_description(),

    install_requires=[
        'Django==1.5.12',
        'Fabric==1.6',
        #'Sphinx==1.2b1',
        'numpydoc==0.4',
        'python-memcached==1.58',
        'uwsgi',

        # TODO check deps.
        'django-autocomplete-light==2.0.0a15',
        'configparser==3.5.0',
        'Jinja2==2.9.5',
        'xlrd==1.0.0',
        'xlwt==1.2.0',
        

        # TODO siteskin deps. check actual versions
        'pytils==0.2.3',
        'pytz==2013b',
        'html5lib==0.95',

        # TODO check spicy.core.profile deps.
        #'django-social-auth==0.6.1', 
        'python-social-auth==0.2.13',
        'Pillow==3.4.2',
        'django-simple-captcha<0.4.7', 
        
        # debug deps.
        'Fabric==1.6',
        'pycrypto==2.6.1',  # for Fabric API
        'raven==3.2.1',
        'numpydoc==0.4',
        'django-nose==1.2',
        'django-debug-toolbar==0.9.4',
    ],

    dependency_links=[
        #'svn+http://django-simple-captcha.googlecode.com/svn/trunk@54#egg=django-captcha',
        #'git+https://github.com/krvss/django-social-auth.git#egg=django-social-auth-0.7.13.dev',
    ],
    entry_points={
        'console_scripts': [
            'spicy = spicy.script:handle_command_line',
        ],
    },
    classifiers=[
        'Framework :: Django',
        'Development Status :: 1.2.1',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
