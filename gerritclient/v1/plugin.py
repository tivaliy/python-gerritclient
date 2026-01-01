from gerritclient.v1 import base


class PluginClient(base.BaseV1Client):
    api_path = "/plugins/"

    def get_all(self, detailed=False):
        request_path = "{api_path}{all}".format(
            api_path=self.api_path, all="?all" if detailed else ""
        )
        return self.connection.get_request(request_path)

    def get_by_id(self, plugin_id):
        request_path = f"{self.api_path}{plugin_id}/gerrit~status"
        return self.connection.get_request(request_path)

    def enable(self, plugin_id):
        request_path = f"{self.api_path}{plugin_id}/gerrit~enable"
        return self.connection.post_request(request_path, json_data={})

    def disable(self, plugin_id):
        request_path = f"{self.api_path}{plugin_id}"
        return self.connection.delete_request(request_path, data={})

    def reload(self, plugin_id):
        request_path = f"{self.api_path}{plugin_id}/gerrit~reload"
        return self.connection.post_request(request_path, json_data={})

    def install(self, plugin_id, source_type, value):
        """Install a new plugin on the Gerrit server.

        :param plugin_id: Plugin identifier
        :param source_type: Source type: 'file'|'url'
        :param value: Data source value based on source_type:
               - binary data if 'file' source type
               - 'url/path/to/plugin.jar' file as a string if 'url' source type
        """

        if source_type not in ("url", "file"):
            raise ValueError('Source can be either of "url" or "file" types.')
        json_data = {"url": value} if source_type == "url" else None
        data = value if source_type == "file" else None
        # If data value is of binary type then 'Content-Type' in header
        # has to be changed to meet binary data representation format
        headers = {"Content-Type": "multipart/form-data"} if data else None
        request_path = f"{self.api_path}{plugin_id}"
        return self.connection.put_request(
            request_path, data=data, json_data=json_data, headers=headers
        )


def get_client(connection):
    return PluginClient(connection)
