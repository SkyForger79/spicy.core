import os
from importlib import import_module
from setuptools import setup, find_packages

"""
Spicy core package
"""
package_name = "spicy"
package_version = import_module('spicy').__version__

package_description = "spicy core"
package_long_description = "spicy core package"


def get_long_description():
    """Return long description from README.md if it's present
    because it doesn't get installed."""
    try:
        return open('README.md').read()
    except IOError:
        return package_long_description

setup(
    namespace_packages=['spicy'],
    packages=find_packages(),
    # package_dir={
    #     '': 'spicy',
    #     # 'spicy.core': 'spicy/core',
    # },

    include_package_data=True,
    package_data={
        'spicy': ['*']
    },

    zip_safe=False,

    install_requires=[
        'Django==1.4.3',
        'Fabric==1.6',
        'Sphinx==1.2b1',
        'numpydoc==0.4',
        'raven==3.2.1',
        'python-memcached==1.48',

        # utils
        'django-crispy-forms==1.2.5',

        # ?? siteskin deps.
        'pytils==0.2.3',
        'pytz',
        'html5lib==0.95',

        # profile deps.
        'django-simple-captcha',
        'django-social-auth==0.6.1',

        # service deps.
        #

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

    name=package_name,
    version=package_version,
    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description=package_description,
    long_description=get_long_description(),
    license='BSD',
    keywords='django, cms',
    url='http://spicytool.com/',

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
