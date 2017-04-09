#
#    Copyright 2017 Vitalii Kulanov
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json
import os
import requests

import gerritclient

from requests import auth

from gerritclient import error
from gerritclient.common import utils


class APIClient(object):
    """This class handles API requests."""

    def __init__(self, host, port, base_url="/", username=None, password=None):
        self.root = "http://{host}:{port}{base_url}".format(host=host,
                                                            port=port,
                                                            base_url=base_url)
        self._username = username
        self._password = password
        self._session = None

        if self.is_authed:
            self.api_root = self.root + "/a/"
        else:
            self.api_root = self.root + "/"

    @property
    def is_authed(self):
        """Checks whether credentials were passed."""

        return True if self._username and self._password else False

    @staticmethod
    def _make_common_headers():
        """Returns a dict of HTTP headers common for all requests."""

        return {'Content-Type': 'application/json',
                'Accept': 'application/json'}

    def _make_session(self):
        """Initializes a HTTP session."""

        session = requests.Session()
        if self.is_authed:
            session.auth = auth.HTTPDigestAuth(self._username, self._password)
        session.headers.update(self._make_common_headers())
        return session

    @property
    def session(self):
        """Lazy initialization of a session."""

        if self._session is None:
            self._session = self._make_session()
        return self._session

    def delete_request(self, api):
        """Make DELETE request to specific API with some data.

        :param api: API endpoint(path)
        """

        url = self.api_root + api
        resp = self.session.delete(url)
        self._raise_for_status_with_info(resp)

        return self._decode_content(resp)

    def put_request(self, api, data, **params):
        """Make PUT request to specific API with some data.

        :param api: API endpoint (path)
        :param data: Data send in request, will be serialized to JSON
        :param params: Params of query string
        """

        url = self.api_root + api
        data_json = json.dumps(data)
        resp = self.session.put(url, data=data_json, params=params)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    def get_request_raw(self, api, params=None):
        """Make a GET request to specific API and return raw response.

        :param api: API endpoint (path)
        :param params: params passed to GET request
        """

        url = self.api_root + api
        return self.session.get(url, params=params)

    def get_request(self, api, params=None):
        """Make GET request to specific API."""

        params = params or {}
        resp = self.get_request_raw(api, params)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    def post_request_raw(self, api, data=None):
        """Make a POST request to specific API and return raw response.

        :param api: API endpoint (path)
        :param data: data send in request, will be serialized to JSON
        """

        url = self.api_root + api
        data_json = None if data is None else json.dumps(data)

        return self.session.post(url, data=data_json)

    def post_request(self, api, data=None):
        """Make POST request to specific API with some data."""

        resp = self.post_request_raw(api, data)
        self._raise_for_status_with_info(resp)
        return self._decode_content(resp)

    @staticmethod
    def _raise_for_status_with_info(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise error.HTTPError(error.get_full_error_message(e))

    @staticmethod
    def _decode_content(response):
        if response.status_code == 204:
            return {}
        if response.status_code == 200:
            # Remove ")]}'" prefix from response, that is used to prevent XSSI
            return json.loads(response.content.strip(")]}'"))
        return response.json()


def get_settings(file_path=None):
    """Gets gerritclient configuration from 'settings.yaml' file.

    If path to configuration 'settings.yaml' file not specified then current
    working directory will be used instead
    """

    if file_path is None:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.yaml')
    try:
        config_data = utils.read_from_file(file_path)
    except (OSError, IOError):
        msg = "Could not read settings from {0}".format(file_path)
        raise error.InvalidFileException(msg)
    return config_data


def connect(host, port, base_url="/", username=None, password=None):
    """Creates API connection."""

    return APIClient(host, port, base_url=base_url,
                     username=username, password=password)


def get_client(resource, version='v1', connection=None):
    """Gets an API client for a resource

    python-gerritclient provides access to Gerrit Code Review's API
    through a set of per-resource facades. In order to get a proper facade
    it's necessary to specify the name and the version of the API.

    :param resource: Name of the resource to get a facade for
    :type resource:  str
    :param version:  Version of the API
    :type version:   str,
                     Available: v1. Default: v1.
    :param connection: API connection
    :type connection: gerritclient.client.APIClient
    :return:         Facade to the specified resource that wraps
                     calls to the specified version of the API.
    """

    # from gerritclient import v1

    version_map = {
        'v1': {
            'plugin': gerritclient.v1.plugin
        }
    }

    try:
        return version_map[version][resource].get_client(connection)
    except KeyError:
        msg = 'Cannot load API client for "{r}" in the API version "{v}".'
        raise ValueError(msg.format(r=resource, v=version))
