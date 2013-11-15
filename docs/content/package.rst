Spicy package structure
=======================

The last version of `spicy` packages structure:

- **spicy**
   - setup.py
   - README.rst
   - **spicy**
      - __init__.py
      - **core**
         - admin
         - profile
         - etc ...
      - **docs**
         - index.rst
         - Makefile
         - conf.py



In ``setup.py`` we using `setuptools`::

   from setuptools import setup

Most part of setup was adapted from **Django** package sources.

Content of `__init__.py` in ``spicy`` catalog::

   __import__('pkg_resources').declare_namespace(__name__)
   VERSION = (1, 1)

   def get_version():
       return '.'.join([str(x) for x in VERSION])

In first line we declaring a namespace of package, it's needed for subpackages properly working.
Second line declares `VERSION` tuple var. Next function `get_version()` resolves it
into dot-splitted string like **1.1**.

Functions `fullsplit()`, `is_package()` and `os.walk()` loop used from Django sources.

Next we call function `setup()` as usual, passing results of loop.
