Spicy commands reference
========================

This page contains a list of `spicy` script commands

.. glossary::

   build-docs

      Building documents for given apps

      .. code-block:: bash

         spicy build-docs --apps app1,appN

   upload-docs

     Uploads documents for given apps to remote server. Documents must be already builded.

     .. code-block:: bash

        spicy upload-docs --apps app1,appN, --host hostname --port 9000 --user user --path remote/path

   create-app

      Creates new `spicy` app in current dir.

      .. code-block:: bash

         spicy create-app appname -d description


Application template
********************

Application would be created from `app` dir of spicy source catalog. Files with extensions `*.py` would be processed for replacing context variables. Template vars placements looks like `${VARNAME}` and are case-sensitive.


Autodoc section
***************

.. automodule:: spicy.script
   :members:
