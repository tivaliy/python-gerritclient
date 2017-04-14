[![Build Status](https://travis-ci.org/tivaliy/python-gerritclient.svg?branch=master)](https://travis-ci.org/tivaliy/python-gerritclient)

# python-gerritclient
CLI tool for Gerrit Code Review system based on REST API

## Quick Start
1. Clone `python-gerritclient` repository: `git clone https://github.com/tivaliy/python-gerritclient.git`.
2. Configure `settings.yaml` file (in `gerritclient/settings.yaml`) to meet your requirements.

    ```yaml
       host: review.example.com
       port: "80"
       base_url: ""
       username: admin
       password: "1234567890aaWmmflSl+ZlOPs23Dffn"
    ```

    Note, `base_url` can be used if your Gerrit Code Review does not sit at the root of the domain, e.g. if `http://example.com/gerrit` then `base_url="/gerrit"`.

3. Create isolated Python environment `virtualenv gerritclient_venv` and activate it `source gerritclient_venv/bin/activate`.
4. Install `python-gerritclient` with all necessary dependencies: `pip install python-gerritclient/.`.
5. Run `gerrit` command with required options, e.g. `gerrit plugin list`. To see all available commands run `gerrit --help`.
