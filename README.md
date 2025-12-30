[![PyPI](https://img.shields.io/pypi/v/python-gerritclient.svg)](https://pypi.python.org/pypi/python-gerritclient)
[![Build Status](https://travis-ci.org/tivaliy/python-gerritclient.svg?branch=master)](https://travis-ci.org/tivaliy/python-gerritclient)
[![Documentation Status](https://readthedocs.org/projects/python-gerritclient/badge/?version=latest)](http://python-gerritclient.readthedocs.io/en/latest/?badge=latest)

# python-gerritclient
CLI tool and Python API wrapper for Gerrit Code Review

## Requirements

**Python 3.11+** is required. This project uses modern Python features and tooling.

## Quick Start

### Command Line Tool (Recommended: Using UV)

[UV](https://docs.astral.sh/uv/) is a fast, modern Python package manager. Recommended for the best experience.

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/tivaliy/python-gerritclient.git
   cd python-gerritclient
   ```

3. Configure `settings.yaml` file (in `gerritclient/settings.yaml`):
    ```yaml
    url: http://review.example.com
    auth_type: basic
    username: admin
    password: "1234567890aaWmmflSl+ZlOPs23Dffn"
    ```

    * `url` - Gerrit server URL in format `<scheme>://<host>:<port>` (e.g., `https://review.openstack.org`)
    * `auth_type` - HTTP authentication scheme (`basic` or `digest`), omit for anonymous access
    * `username` and `password` - user credentials from Gerrit (Settings → HTTP Password)

4. Install dependencies and run:
   ```bash
   uv sync
   uv run gerrit --help
   ```

5. Run commands:
   ```bash
   uv run gerrit plugin list
   uv run gerrit account list "john"
   ```

### Command Line Tool (Alternative: Using pip)

1. Clone the repository:
   ```bash
   git clone https://github.com/tivaliy/python-gerritclient.git
   cd python-gerritclient
   ```

2. Configure `settings.yaml` (same as above)

3. Install with pip:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

4. Run commands:
   ```bash
   gerrit --help
   gerrit plugin list
   ```

### Library Usage

Install the package:
```bash
# With UV
uv add python-gerritclient

# With pip
pip install python-gerritclient
```

```python
from gerritclient import client

connection = client.connect("review.openstack.org", auth_type="digest" username="user-name", password="password")
group_client = client.get_client('group', connection=connection)
members = group_client.get_group_members('swift-core')  # or get_group_members(24)
print(', '.join(member['name'] for member in members))
```

Output result: `Alistair Coles, Christian Schwede, Clay Gerrard, Darrell Bishop, David Goetz, Greg Lange, Janie Richling, John Dickinson, Kota Tsuyuzaki, Mahati Chamarthy, Matthew Oliver, Michael Barton, Pete Zaitcev, Samuel Merritt, Thiago da Silva, Tim Burke`
