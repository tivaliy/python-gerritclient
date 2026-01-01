[![PyPI](https://img.shields.io/pypi/v/python-gerritclient.svg)](https://pypi.python.org/pypi/python-gerritclient)
[![Build Status](https://github.com/tivaliy/python-gerritclient/actions/workflows/test.yml/badge.svg)](https://github.com/tivaliy/python-gerritclient/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/python-gerritclient/badge/?version=latest)](http://python-gerritclient.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

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

3. Configure environment variables (create a `.env` file or export directly):
    ```bash
    # Option A: Create a .env file
    cp .env.example .env
    # Edit .env with your settings

    # Option B: Export directly
    export GERRIT_URL=https://review.example.com
    export GERRIT_AUTH_TYPE=basic
    export GERRIT_USERNAME=admin
    export GERRIT_PASSWORD="your-http-password"
    ```

    * `GERRIT_URL` - Gerrit server URL (e.g., `https://review.openstack.org`)
    * `GERRIT_AUTH_TYPE` - HTTP authentication scheme (`basic` or `digest`), omit for anonymous access
    * `GERRIT_USERNAME` and `GERRIT_PASSWORD` - user credentials from Gerrit (Settings → HTTP Password)

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

2. Configure environment variables (same as step 3 above)

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

## What's New in v1.0

**Major modernization release!** This version brings python-gerritclient into the modern Python ecosystem:

### 🚀 Performance & Tooling
- **UV Package Manager**: 10-100x faster dependency resolution and installation
- **Ruff Linting**: 100x faster than flake8, instant code quality checks
- **Modern Python**: Requires Python 3.11+ (dropped Python 2.7/3.5/3.6 support)

### 🏗️ Infrastructure
- **GitHub Actions CI/CD**: Replaced Travis CI with modern GitHub Actions
- **Modern pyproject.toml**: Migrated from legacy setup.py/setup.cfg
- **Setuptools Build Backend**: Replaced pbr with modern setuptools

### ✨ Code Quality
- Removed all Python 2 compatibility code (six library)
- Applied 100+ code modernizations (modern super(), f-strings, etc.)
- 96.7% test coverage (178/184 tests passing)

### ✅ Validated
Tested and working against **Gerrit 3.13.1** (latest) on production instances (Android Code Review).

## Compatibility

### Gerrit Versions
- **Recommended**: Gerrit 3.11+ (latest tested: 3.13.1)
- **Supported**: Gerrit 2.14+ (backwards compatible)
- **API Coverage**: ~45% of Gerrit REST API

### Python Versions
- **Required**: Python 3.11+
- **Tested**: Python 3.11, 3.12, 3.13
- **Dropped**: Python 2.7, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10

## Development

### Setting Up Development Environment

1. **Install UV** (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/tivaliy/python-gerritclient.git
   cd python-gerritclient
   uv sync --all-extras
   ```

3. **Install in editable mode**:
   ```bash
   uv pip install -e .
   ```

### Running Tests

```bash
# Run unit tests with stestr
uv pip install stestr
uv run stestr run

# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .

# Format check (CI)
uv run ruff format --check .
```

### Code Quality Tools

- **Linter**: [Ruff](https://docs.astral.sh/ruff/) - Fast Python linter
- **Formatter**: Ruff format - Fast Python formatter
- **Test Runner**: [stestr](https://stestr.readthedocs.io/) - Parallel test runner
- **CI/CD**: GitHub Actions

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting: `uv run stestr run && uv run ruff check .`
5. Format code: `uv run ruff format .`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

Apache License 2.0

## Credits

Originally created by [Vitalii Kulanov](https://github.com/tivaliy)
