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

from gerritclient.v1 import base


class PluginClient(base.BaseV1Client):

    api_path = "plugins/"

    def get_all(self, detailed=False):
        request_path = "{api_path}{all}".format(
            api_path=self.api_path,
            all="?all" if detailed else "")
        return self.connection.get_request(request_path)

    def get_by_id(self, plugin_id):
        request_path = "{api_path}{plugin_id}/gerrit~status".format(
            api_path=self.api_path,
            plugin_id=plugin_id)
        return self.connection.get_request(request_path)

    def enable(self, plugin_id):
        request_path = "{api_path}{plugin_id}/gerrit~enable".format(
            api_path=self.api_path,
            plugin_id=plugin_id)
        return self.connection.post_request(request_path, json_data={})

    def disable(self, plugin_id):
        request_path = "{api_path}{plugin_id}".format(
            api_path=self.api_path,
            plugin_id=plugin_id)
        return self.connection.delete_request(request_path, data={})


def get_client(connection):
    return PluginClient(connection)
