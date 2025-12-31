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

Configuration
~~~~~~~~~~~~~

Configuration is loaded from environment variables with the ``GERRIT_`` prefix.

**Using environment variables** (recommended for CI/CD)::

    export GERRIT_URL=https://review.example.com
    export GERRIT_AUTH_TYPE=basic
    export GERRIT_USERNAME=your-username
    export GERRIT_PASSWORD=your-http-password

**Using a .env file** (recommended for local development)::

    # Create a .env file in your project directory
    GERRIT_URL=https://review.example.com
    GERRIT_AUTH_TYPE=basic
    GERRIT_USERNAME=your-username
    GERRIT_PASSWORD=your-http-password

**Configuration options:**

* ``GERRIT_URL`` (required): Gerrit server URL (e.g., ``https://review.openstack.org``)
* ``GERRIT_AUTH_TYPE`` (optional): Authentication type - ``basic`` or ``digest``. Omit for anonymous access.
* ``GERRIT_USERNAME`` (required if auth_type set): Your Gerrit username
* ``GERRIT_PASSWORD`` (required if auth_type set): HTTP password from Gerrit (Settings -> HTTP Credentials)

Basic Usage
~~~~~~~~~~~

Command line::

    gerrit --help
    gerrit server version
    gerrit change list "status:open"

Python API::

    from gerritclient import client

    # Option 1: Use environment variables (automatic)
    group_client = client.get_client('group')
    members = group_client.get_group_members('core-team')

    # Option 2: Explicit connection
    connection = client.connect(
        "https://review.example.com",
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
