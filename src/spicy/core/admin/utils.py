import os
import sys
import codecs

from . import defaults

def get_themes_from_path(path, version=None):
    """

    look in for ``spicy.theme`` file inside all subdirectories in the defined ``path``

    param path: abs path with spicy.* themes 
    param version: hash key (revision key for product)

    spicy.ecom>=asdaLKJD823123kjsadSDaslkasd
    spicy.light==asdkasdlkj1231lkh23jkhadasd
    spicy.media<=asdkjalhskd1239123lkjadssda
    """

    try:
        #for theme in os.path.walk(path, get_theme_dir, None):

        for theme in os.listdir(path):
           if os.path.isdir(theme):
               if defaults.SPICY_THEME_FILE in os.listdir(theme):
                   # TODO
                   # check theme version compatibility
                   
                   return (theme, os.path.join(defaults.THEMES_PATH, theme))
    except OSError:
        return []
