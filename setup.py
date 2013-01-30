# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
from os.path import join, dirname
from setuptools import setup, find_packages

version = __import__('spicy').__version__

LONG_DESCRIPTION = """
Django extension toolkit
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


setup(name='spicy',
      version=version,
      author='Burtsev Alexander',
      author_email='eburus@gmail.com',
      description='Spicy',
      license='BSD',
      keywords='django, cms',
      url='',
      scripts = ('bin/spicy.py',),      
      #download_url='',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      #tests_require=[
      #  'django>=1.3,<1.5',
      #  ],
      #test_suite='runtests.runtests',
      
      long_description=long_description(),
      install_requires=['django>=1.3.1',
                        'django-nose',
                        'rudolf',
                        'pytils',
                        'fabric',
                        'pytz',
                        ],

      classifiers=['Framework :: Django',
                   'Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7'])
