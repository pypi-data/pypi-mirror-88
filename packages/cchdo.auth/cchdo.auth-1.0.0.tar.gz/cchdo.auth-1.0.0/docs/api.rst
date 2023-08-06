API Reference
=============

Public
------

.. py:data:: cchdo.auth.dirs
   :type: appdirs.AppDirs

   The preconfigured AppDirs instance which has the following read only properties:

   * ``user_data_dir``
   * ``user_config_dir``
   * ``user_cache_dir``
   * ``site_data_dir``
   * ``site_config_dir``
   * ``user_log_dir``

   The actual values are platform dependent.

.. py:data:: cchdo.auth.CONFIG_FILE
   :type: str

   A string containing the path to the config file on the running platform.

   example in the devcontainer (linux):

   >>> from cchdo.auth import CONFIG_FILE
   >>> CONFIG_FILE
   '/home/vscode/.config/edu.ucsd.cchdo/config.cfg'

.. automodule:: cchdo.auth
   :members:
   :undoc-members:


Private
-------
.. automodule:: cchdo.auth
   :members:
   :exclude-members: CCHDOAuth, get_apikey
   :private-members:
   :undoc-members:
   :noindex: