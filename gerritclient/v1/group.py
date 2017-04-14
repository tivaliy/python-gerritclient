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


class GroupClient(base.BaseV1Client):

    api_path = "groups/"

    def get_all(self):
        return self.connection.get_request(self.api_path)

    def get_by_entity_id(self, entity_id, detailed=False):
        request_path = "{api_path}{entity_id}/{detail}".format(
            api_path=self.api_path,
            entity_id=entity_id,
            detail="detail" if detailed else "")
        return self.connection.get_request(request_path)

    def get_group_members(self, entity_id, show_all=False):
        request_path = "{api_path}{entity_id}/members/{all}".format(
            api_path=self.api_path,
            entity_id=entity_id,
            all="?recursive" if show_all else "")
        return self.connection.get_request(request_path)


def get_client(connection):
    return GroupClient(connection)
