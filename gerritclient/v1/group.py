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

    def get_by_id(self, group_id, detailed=False):
        request_path = "{api_path}{group_id}/{detail}".format(
            api_path=self.api_path,
            group_id=group_id,
            detail="detail" if detailed else "")
        return self.connection.get_request(request_path)

    def get_members(self, group_id, detailed=False):
        request_path = "{api_path}{group_id}/members/{all}".format(
            api_path=self.api_path,
            group_id=group_id,
            all="?recursive" if detailed else "")
        return self.connection.get_request(request_path)

    def add_members(self, group_id, accounts_ids):
        """Adds user(s) as member to a Gerrit internal group.

        :param group_id: Group identifier
        :param accounts_ids: A list of accounts identifiers
        :return: A list of detailed AccountInfo entities that describes
                 the group members that were specified
        """

        data = {'members': accounts_ids}
        request_path = "{api_path}{group_id}/members".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.post_request(request_path, json_data=data)

    def rename(self, group_id, new_name):
        data = {"name": new_name}
        request_path = "{api_path}{group_id}/name".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.put_request(request_path, json_data=data)

    def set_description(self, group_id, description):
        data = {"description": description}
        request_path = "{api_path}{group_id}/description".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.put_request(request_path, json_data=data)

    def delete_description(self, group_id):
        request_path = "{api_path}{group_id}/description".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.delete_request(request_path, data={})

    def set_options(self, group_id, visibility):
        """Set the options of a Gerrit internal group.

        :param group_id: Identifier of a group
                        (UUID|legacy numeric ID|name of the group)
        :type group_id: str
        :param visibility: Whether the group is visible to all registered users
        :type visibility: bool
        :return The new group options are returned as a dict
        """

        data = {'visible_to_all': visibility}
        request_path = "{api_path}{group_id}/options".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.put_request(request_path, json_data=data)

    def set_owner_group(self, group_id, owner_group):

        data = {'owner': owner_group}
        request_path = "{api_path}{group_id}/owner".format(
            api_path=self.api_path,
            group_id=group_id)
        return self.connection.put_request(request_path, json_data=data)


def get_client(connection):
    return GroupClient(connection)
