# coding: utf-8
"""
spicy core package
"""
from setuptools import setup, find_packages


long_description = """
spicy core package
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open('README.rst').read()
    except IOError:
        return long_description

setup(
    name='spicy',
    version='1.1',
    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description='spicy',
    license='BSD',
    keywords='django, cms',
    url='',

    packages=find_packages('src'),
    package_dir={
        '': 'src',
        'spicy.core': 'src/spicy/core',
        'spicy.core.service': 'src/spicy/core/service',
        'spicy.core.profile': 'src/spicy/core/profile',
        'spicy.core.admin': 'src/spicy/core/admin',
        'spicy.core.siteskin': 'src/spicy/core/siteskin',
        'spicy.core.rmanager': 'src/spicy/core/rmanager',
        'spicy.utils': 'src/spicy/utils',
    },
    include_package_data=True,
    zip_safe=True,

    long_description=long_description(),

    install_requires=[
        'Django==1.4.3',
        'fabric==1.6',
        'Sphinx==1.2b1',
        'raven==3.2.1',
        'python-memcached==1.48',

        # ?? siteskin deps.
        'pytils==0.2.3',
        'pytz',

        # profile deps.
        'django-captcha==0.1.7-r54.dev',

        # service deps.
        #

    ],
    dependency_links=[
        'svn+http://django-simple-captcha.googlecode.com/svn/trunk@54#egg=django-captcha-0.1.7-r54.dev'
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
