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

import abc
import six

from requests import utils as requests_utils

from gerritclient import client


@six.add_metaclass(abc.ABCMeta)
class BaseV1Client(object):

    @abc.abstractproperty
    def api_path(self):
        pass

    def __init__(self, connection=None):
        if connection is None:
            config = client.get_settings()
            connection = client.connect(**config)
        self.connection = connection


@six.add_metaclass(abc.ABCMeta)
class BaseV1ClientCreateEntity(BaseV1Client):

    def create(self, entity_id, data=None):
        """Create a new entity."""

        data = data if data else {}
        request_path = "{api_path}{entity_id}".format(
            api_path=self.api_path,
            entity_id=requests_utils.quote(entity_id, safe=''))
        return self.connection.put_request(request_path, json_data=data)
