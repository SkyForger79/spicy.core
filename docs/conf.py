# -*- coding: utf-8 -*-
"""
SpicyCMS Mediacenter module documentation build configuration file
"""
import os
import sys
import spicy


sys.path.append(os.path.abspath('../spicy'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'numpydoc',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Spicy Tool'
copyright = '2013, SpicyTeam'


_spicy_version = spicy.get_version()
version = str(_spicy_version)
release = str('%s-dev' % (version)) # TODO: how would we name releases?

exclude_patterns = ['_build']
pygments_style = 'manni'
html_theme = 'nature'
html_static_path = ['_static']
# htmlhelp_basename = 'SpicyCMSMediacenterdoc'

# latex_elements = {}
# latex_documents = [
#     ('index',
#      'SpicyCMSMediacenter.tex',
#      'SpicyCMS Mediacenter Documentation',
#      'SpicyTeam',
#      'manual'),
# ]
# man_pages = [
#     ('index', 'spicycmslight', 'SpicyCMS Light Documentation',
#      ['SpicyTeam'], 1)
# ]
# texinfo_documents = [
#   ('index', 'SpicyCMSLight', 'SpicyCMS Light Documentation',
#    'SpicyTeam', 'SpicyCMSLight', 'One line description of project.',
#    'Miscellaneous'),
# ]
