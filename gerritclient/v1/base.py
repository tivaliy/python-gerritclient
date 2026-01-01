import abc

from requests import utils as requests_utils

from gerritclient import client


class BaseV1Client(abc.ABC):
    @property
    @abc.abstractmethod
    def api_path(self):
        pass

    def __init__(self, connection=None):
        if connection is None:
            config = client.get_settings()
            connection = client.connect(**config)
        self.connection = connection


class BaseV1ClientCreateEntity(BaseV1Client):
    def create(self, entity_id, data=None):
        """Create a new entity."""

        data = data if data else {}
        request_path = "{api_path}{entity_id}".format(
            api_path=self.api_path, entity_id=requests_utils.quote(entity_id, safe="")
        )
        return self.connection.put_request(request_path, json_data=data)
