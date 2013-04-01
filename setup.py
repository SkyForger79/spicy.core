# coding: utf-8
"""
Setup file for easy Spicy installation
"""
from setuptools import setup, find_packages


LONG_DESCRIPTION = """
Spicy toolkit main package
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open('README.rst').read()
    except IOError:
        return LONG_DESCRIPTION

setup(
    name='spicy',
    version='1.1',
    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description='Spicy',
    license='BSD',
    keywords='django, cms',
    url='',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=True,

    long_description=long_description(),

    install_requires=[
        'django==1.4.3',
        'fabric==1.6',
        'raven==3.2.1',
        'python-memcached==1.48',
        'pytils==0.2.3',
        'pytz',
    ],

    entry_points={
        'console_scripts': [
            'spicy = spicy:handle_command_line',
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
