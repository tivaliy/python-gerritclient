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


class ChangeClient(base.BaseV1Client):

    api_path = "changes/"

    def get_all(self, query, options=None, limit=None, skip=None):
        """Query changes.

        :param query: Queries as a list of string
        :param options: List of options to fetch additional data about changes
        :param limit: Int value that allows to limit the number of changes
                      to be included in the output results
        :param skip: Int value that allows to skip the given number of
                     changes from the beginning of the list
        :return A list of ChangeInfo entries
        """

        params = {k: v for k, v in (('o', options),
                                    ('n', limit),
                                    ('S', skip)) if v is not None}
        request_path = "{api_path}{query}".format(
            api_path=self.api_path,
            query="?q={query}".format(query='&q='.join(query)))
        return self.connection.get_request(request_path, params=params)

    def get_by_id(self, change_id, detailed=False, options=None):
        """Retrieve a change.

        :param change_id: Identifier that uniquely identifies one change.
        :param detailed: boolean value, if True then retrieve a change with
                         labels, detailed labels, detailed accounts,
                         reviewer updates, and messages.
        :param options: List of options to fetch additional data about a change
        :return: ChangeInfo entity is returned that describes the change.
        """

        params = {'o': options}
        request_path = "{api_path}{change_id}/{detail}".format(
            api_path=self.api_path,
            change_id=change_id,
            detail="detail" if detailed else "")
        return self.connection.get_request(request_path, params=params)

    def get_topic(self, change_id):
        """Retrieve the topic of a change."""

        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path,
            change_id=change_id)
        return self.connection.get_request(request_path)


def get_client(connection):
    return ChangeClient(connection)
