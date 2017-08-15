===========================
Gerrit Command Line Utility
===========================

`python-gerritclient` CLI is a command line utility for managing Gerrit
Code Review environment. It allows to perform several types of operations.

For help on a specific :command:`gerrit` command or subcommand, enter:

.. code-block:: console

   $ gerrit COMMAND [SUBCOMMAND [SUBCOMMAND ...]] --help

All :command:`gerrit` commands support several options:

.. code-block:: console

   Usage: gerrit [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

**optional arguments:**

``--version``
  Show program's version number and exit.

``-v, --verbose``
  Increase verbosity of output. Can be repeated.

``-q, --quiet``
  Suppress output except warnings and errors.

``--log-file LOG_FILE``
  Specify a file to log output. Disabled by default.

``-h, --help``
  Show help message and exit.

``--debug``
  Show tracebacks on errors.

Gerrit CLI Commands
-------------------

.. toctree::
   :maxdepth: 1

   account
   change
   group
   plugin
   project
   server
