[![Build Status](https://travis-ci.org/tivaliy/python-gerritclient.svg?branch=master)](https://travis-ci.org/tivaliy/python-gerritclient)

# python-gerritclient
CLI tool and Python API wrapper for Gerrit Code Review

## Quick Start

### Command Line Tool
1. Clone `python-gerritclient` repository: `git clone https://github.com/tivaliy/python-gerritclient.git`.
2. Configure `settings.yaml` file (in `gerritclient/settings.yaml`) to meet your requirements.

    ```yaml
       url: http://review.example.com
       auth_type: basic
       username: admin
       password: "1234567890aaWmmflSl+ZlOPs23Dffn"
    ```

    * `url` can be specified according to the following format `<scheme>://<host>:<port>`, e.g. `https://review.openstack.org`
    * `auth_type` specifies HTTP authentication scheme (`basic` or `digest`), can be omitted, then all requests will be anonymous with respective restrictions
    * `username` and `password` - user credentials from Gerrit system (Settings &#8594; HTTP Password)

3. Create isolated Python environment `virtualenv gerritclient_venv` and activate it `source gerritclient_venv/bin/activate`.
4. Install `python-gerritclient` with all necessary dependencies: `pip install python-gerritclient/.`.
5. (Optional) Add gerrit command bash completion `gerrit complete | sudo tee /etc/bash_completion.d/gc.bash_completion > /dev/null`
6. Run `gerrit` command with required options, e.g. `gerrit plugin list`. To see all available commands run `gerrit --help`.

### Library
1. Clone `python-gerritclient` repository: `git clone https://github.com/tivaliy/python-gerritclient.git`.
2. Create isolated Python environment `virtualenv gerritclient_venv` and activate it `source gerritclient_venv/bin/activate`.
3. Install `python-gerritclient` with all necessary dependencies: `pip install python-gerritclient/.`.

```python
from gerritclient import client

connection = client.connect("review.openstack.org", auth_type="digest" username="user-name", password="password")
group_client = client.get_client('group', connection=connection)
members = group_client.get_group_members('swift-core')  # or get_group_members(24)
print(', '.join(member['name'] for member in members))
```

Output result: `Alistair Coles, Christian Schwede, Clay Gerrard, Darrell Bishop, David Goetz, Greg Lange, Janie Richling, John Dickinson, Kota Tsuyuzaki, Mahati Chamarthy, Matthew Oliver, Michael Barton, Pete Zaitcev, Samuel Merritt, Thiago da Silva, Tim Burke`
