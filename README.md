[![Build Status](https://travis-ci.org/tivaliy/python-gerritclient.svg?branch=master)](https://travis-ci.org/tivaliy/python-gerritclient)

# python-gerritclient
CLI tool for Gerrit Code Review system based on REST API

## Quick Start

### Command Line Tool
1. Clone `python-gerritclient` repository: `git clone https://github.com/tivaliy/python-gerritclient.git`.
2. Configure `settings.yaml` file (in `gerritclient/settings.yaml`) to meet your requirements.

    ```yaml
       host: review.example.com
       port: "80"
       base_url: ""
       username: admin
       password: "1234567890aaWmmflSl+ZlOPs23Dffn"
    ```

    * `base_url` can be used if your Gerrit Code Review does not sit at the root of the domain, e.g. if `http://example.com/gerrit` then `base_url="/gerrit"`.
    * `username` and `password` can be omitted then all requests will be anonymous with respective restrictions

3. Create isolated Python environment `virtualenv gerritclient_venv` and activate it `source gerritclient_venv/bin/activate`.
4. Install `python-gerritclient` with all necessary dependencies: `pip install python-gerritclient/.`.
5. Run `gerrit` command with required options, e.g. `gerrit plugin list`. To see all available commands run `gerrit --help`.

### Library
1. Clone `python-gerritclient` repository: `git clone https://github.com/tivaliy/python-gerritclient.git`.
2. Create isolated Python environment `virtualenv gerritclient_venv` and activate it `source gerritclient_venv/bin/activate`.
3. Install `python-gerritclient` with all necessary dependencies: `pip install python-gerritclient/.`.

```python
from gerritclient import client

connection = client.connect("review.openstack.org", "80", username="user-name", password="password")
group_client = client.get_client('group', connection=connection)
members = group_client.get_group_members('swift-core')  # or get_group_members(24)
print(', '.join(member['name'] for member in members))
```

Output result: `Alistair Coles, Christian Schwede, Clay Gerrard, Darrell Bishop, David Goetz, Greg Lange, Janie Richling, John Dickinson, Kota Tsuyuzaki, Mahati Chamarthy, Matthew Oliver, Michael Barton, Pete Zaitcev, Samuel Merritt, Thiago da Silva, Tim Burke`
