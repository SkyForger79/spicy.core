#!/usr/bin/env python
"""
Setup file for easy Spicy installation
"""

from __future__ import unicode_literals

from os.path import join, dirname
from setuptools import setup, find_packages


version = __import__('spicy').__version__

LONG_DESCRIPTION = """
Spicy toolkit main package
"""

def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION

setup(
    name='spicy',
    version=version,
    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description='Spicy',
    license='BSD',
    keywords='django, cms',
    url='',

    packages=find_packages(),
    # package_dir={'': 'src/spicy'},
    include_package_data=True,
    zip_safe=False,

    long_description=long_description(),

    install_requires=[
        'setuptools',
        'django==1.4.3',
        'pytils',
        'fabric',
        'pytz',
        'raven',
        'python-memcached',
    ],

    entry_points = {
        'console_scripts': [
            'spicy = spicy:handle_command_line',
        ],
    },

    classifiers=[
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
