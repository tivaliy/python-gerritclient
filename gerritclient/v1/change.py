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

from requests import utils as requests_utils

from gerritclient.v1 import base


class ChangeClient(base.BaseV1Client):

    api_path = "/changes/"

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
            change_id=requests_utils.quote(change_id, safe=''),
            detail="detail" if detailed else "")
        return self.connection.get_request(request_path, params=params)

    def create(self, data):
        """Create a new change."""

        return self.connection.post_request(self.api_path, json_data=data)

    def delete(self, change_id):
        """Delete a change."""

        request_path = "{api_path}{change_id}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.delete_request(request_path, data={})

    def abandon(self, change_id):
        """Abandon a change."""

        request_path = "{api_path}{change_id}/abandon".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data={})

    def restore(self, change_id):
        """Restore a change."""

        request_path = "{api_path}{change_id}/restore".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data={})

    def revert(self, change_id, message=None):
        """Revert a change."""

        data = {k: v for k, v in (('message', message),) if v is not None}
        request_path = "{api_path}{change_id}/revert".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data=data)

    def rebase(self, change_id, parent=None):
        """Rebase a change."""

        data = {k: v for k, v in (('base', parent),) if v is not None}
        request_path = "{api_path}{change_id}/rebase".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data=data)

    def move(self, change_id, branch, message=None):
        """Move a change."""

        data = {k: v for k, v in (('destination_branch', branch),
                                  ('message', message)) if v is not None}
        request_path = "{api_path}{change_id}/move".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data=data)

    def submit(self, change_id, on_behalf_of=None, notify=None):
        """Submit a change."""

        # TODO(vkulanov): add 'notify_details' field (parameter) support
        data = {k: v for k, v in (('on_behalf_of', on_behalf_of),
                                  ('notify', notify)) if v is not None}
        request_path = "{api_path}{change_id}/submit".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data=data)

    def get_topic(self, change_id):
        """Retrieve the topic of a change."""

        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.get_request(request_path)

    def set_topic(self, change_id, topic):
        """Set the topic of a change."""

        data = {'topic': topic}
        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def delete_topic(self, change_id):
        """Delete the topic of a change."""

        request_path = "{api_path}{change_id}/topic".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.delete_request(request_path, data={})

    def get_assignee(self, change_id):
        """Retrieve the account of the user assigned to a change."""

        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.get_request(request_path)

    def get_assignees(self, change_id):
        """Retrieve a list of every user ever assigned to a change."""

        request_path = "{api_path}{change_id}/past_assignees".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.get_request(request_path)

    def set_assignee(self, change_id, account_id):
        """Set the assignee of a change."""

        data = {'assignee': account_id}
        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def delete_assignee(self, change_id):
        """Delete the assignee of a change."""

        request_path = "{api_path}{change_id}/assignee".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.delete_request(request_path, data={})

    def publish_draft(self, change_id):
        """Publish a draft change."""

        request_path = "{api_path}{change_id}/publish".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data={})

    def get_included(self, change_id):
        """Retrieve the branches and tags in which a change is included."""

        request_path = "{api_path}{change_id}/in".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.get_request(request_path)

    def index(self, change_id):
        """Add or update the change in the secondary index."""

        request_path = "{api_path}{change_id}/index".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data={})

    def get_comments(self, change_id, comment_type=None):
        """List the published comments of all revisions of the change.

        :param change_id: Identifier that uniquely identifies one change.
        :param comment_type: Type of comments (None|'drafts'|'robotcomments')
                             None - published comments,
                             'drafts' - draft comments,
                             'robotcomments' - robotcomments.
        :return A list of CommentInfo entries.
        """

        request_path = "{api_path}{change_id}/{comment_type}".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''),
            comment_type='comments' if not comment_type else comment_type)
        return self.connection.get_request(request_path)

    def check_consistency(self, change_id):
        """Perform consistency checks on the change."""

        request_path = "{api_path}{change_id}/check".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.get_request(request_path)

    def fix_consistency(self, change_id, is_delete=False,
                        expect_merged_as=False):
        """Perform consistency checks on the change and fixes any problems.

        :param change_id: Identifier that uniquely identifies one change.
        :param is_delete: If True, delete patch sets from the database
                          if they refer to missing commit options.
        :param expect_merged_as: If True, check that the change is merged into
                                 the destination branch as this exact SHA-1.
                                 If not, insert a new patch set referring to
                                 this commit.
        :return Returns a ChangeInfo entity with the problems field values
                that reflect any fixes.
        """

        data = {'delete_patch_set_if_commit_missing': is_delete,
                'expect_merged_as': expect_merged_as}
        request_path = "{api_path}{change_id}/check".format(
            api_path=self.api_path,
            change_id=requests_utils.quote(change_id, safe=''))
        return self.connection.post_request(request_path, json_data=data)


def get_client(connection):
    return ChangeClient(connection)
