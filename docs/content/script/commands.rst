Spicy command reference
----------------------------

.. glossary::

   build-docs

      Building and uploads documents to remote documantation server

   create-app

      Creates new `spicy` app in current dir.

      .. code-block:: bash

         spicy create-app appname -d description


Application template
++++++++++++++++++++

Application would be created from `app` dir of spicy source catalog. Files with extensions `*.py` would be processed for replacing context variables. Template vars placements looks like `${VARNAME}` and are case-sensitive.


Autodoc section
---------------

.. automodule:: spicy.script
   :members:
