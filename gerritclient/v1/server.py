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


class ServerClient(base.BaseV1Client):

    api_path = "/config/server/"

    def get_version(self):
        """Return the version of the Gerrit server."""

        request_path = "{api_path}version".format(api_path=self.api_path)
        return self.connection.get_request(request_path)

    def get_config(self):
        """Return the information about the Gerrit server configuration."""

        request_path = "{api_path}info".format(api_path=self.api_path)
        return self.connection.get_request(request_path)

    def get_capabilities(self):
        """Lists the capabilities that are available in the system."""

        request_path = "{api_path}capabilities".format(api_path=self.api_path)
        return self.connection.get_request(request_path)

    def get_caches(self, formatting=None):
        """List information about all the caches of the server.

        :param formatting: None|'text_list'|'list'
                           'list' - returns the cache names as JSON list;
                           'text_list' - returns the cache names as a UTF-8
                           list that is base64 encoded. The cache names are
                           delimited by '\n'.
        :return An information about caches of the server depend on formatting
        """

        params = {'format': formatting}
        request_path = "{api_path}caches".format(api_path=self.api_path)
        return self.connection.get_request(request_path, params=params)

    def get_cache(self, name):
        """Retrieve information about a specific cache."""

        request_path = "{api_path}caches/{name}".format(api_path=self.api_path,
                                                        name=name)
        return self.connection.get_request(request_path)

    def flush_caches(self, is_all=False, names=None):
        """Flush all/specific cache.

        :param is_all: boolean value, if True then all cache will be flushed
        :param names: list of names of cache to be flushed
        """

        data = {"operation": "FLUSH_ALL" if is_all else "FLUSH",
                "caches": names}
        request_path = "{api_path}caches".format(api_path=self.api_path)
        return self.connection.post_request(request_path, json_data=data)

    def get_summary_state(self, jvm=False, gc=False):
        """Retrieve a summary of the current server state."""

        params = {'jvm': int(jvm), 'gc': int(gc)}
        request_path = "{api_path}summary".format(api_path=self.api_path)
        return self.connection.get_request(request_path, params=params)

    def get_tasks(self):
        """Get all tasks from the background work queues."""

        request_path = "{api_path}tasks".format(api_path=self.api_path)
        return self.connection.get_request(request_path)

    def get_task(self, task_id):
        """Retrieve a task from the background work queue."""

        request_path = "{api_path}tasks/{task_id}".format(
            api_path=self.api_path,
            task_id=task_id)
        return self.connection.get_request(request_path)

    def delete_task(self, task_id):
        """Kill a task from the background work queue."""

        request_path = "{api_path}tasks/{task_id}".format(
            api_path=self.api_path,
            task_id=task_id)
        return self.connection.delete_request(request_path, data={})


def get_client(connection):
    return ServerClient(connection)
