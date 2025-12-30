===================
python-gerritclient
===================

This is a CLI tool and Python API wrapper for
`Gerrit Code Review <https://www.gerritcodereview.com/>`_.

.. note::
   **Version 1.0+** requires **Python 3.11 or higher**.
   Python 2.7 and Python 3.5-3.10 are no longer supported.

Overview
--------

python-gerritclient is a modern Python client for Gerrit Code Review that provides:

* **Command Line Interface**: 88 commands for managing accounts, changes, projects, plugins, and more
* **Python API**: Clean, pythonic interface for programmatic access
* **Modern Tooling**: Built with UV and Ruff for blazing fast performance
* **Production Tested**: Validated against Gerrit 3.13.1 on real-world instances

Compatibility
-------------

**Gerrit Versions:**
  - Recommended: Gerrit 3.11+ (tested with 3.13.1)
  - Supported: Gerrit 2.14+
  - API Coverage: ~45% of Gerrit REST API

**Python Versions:**
  - Required: Python 3.11+
  - Tested: Python 3.11, 3.12, 3.13

Quick Start
-----------

Installation
~~~~~~~~~~~~

Using UV (recommended)::

    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv pip install python-gerritclient

Using pip::

    pip install python-gerritclient

Basic Usage
~~~~~~~~~~~

Command line::

    gerrit --help
    gerrit server version
    gerrit change list "status:open"

Python API::

    from gerritclient import client

    connection = client.connect(
        "review.example.com",
        auth_type="digest",
        username="user",
        password="pass"
    )

    group_client = client.get_client('group', connection=connection)
    members = group_client.get_group_members('core-team')

Documentation
-------------

.. toctree::
   :maxdepth: 3

   cli/index

Additional Resources
--------------------

* `GitHub Repository <https://github.com/tivaliy/python-gerritclient>`_
* `Issue Tracker <https://github.com/tivaliy/python-gerritclient/issues>`_
* `PyPI Package <https://pypi.org/project/python-gerritclient/>`_

License
-------

Apache License 2.0
