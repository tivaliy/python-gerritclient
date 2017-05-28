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


class AccountClient(base.BaseV1Client):

    api_path = "accounts/"

    def get_all(self, query, suggested=False, limit=None, skip=None,
                detailed=False, all_emails=False):
        """Get list of all available accounts visible by the caller.

        :param query: Query string
        :param suggested: boolean value, if True get account suggestions
                          based on query string. If a result limit n is not
                          specified, then the default 10 is used.
        :param limit: Int value that allows to limit the number of accounts
                      to be included in the output results
        :param skip: Int value that allows to skip the given
                     number of accounts from the beginning of the list
        :param detailed: boolean value, if True then full name,
                         preferred email, username and avatars for each account
                         will be added to the output result
        :param all_emails: boolean value, if True then all registered emails
                           for each account will be added to the output result
        :return: List of accounts as a list of dicts
        """

        option = filter(None, ['DETAILS' if detailed else None,
                               'ALL_EMAILS' if all_emails else None])
        option = None if not option else option
        params = {k: v for k, v in (('q', query),
                                    ('n', limit),
                                    ('S', skip),
                                    ('o', option)) if v is not None}
        request_path = "{api_path}{suggest}".format(
            api_path=self.api_path,
            suggest="?suggest" if suggested else "")
        return self.connection.get_request(request_path, params=params)

    def get_by_id(self, account_id, detailed=False):
        """Get data about specific account in Gerrit.

        :param account_id: (account_ID|username|email|name) as a string value
        :param detailed: boolean type, If True then fetch info in more details
        :return: dict, that contains information about account
        """

        request_path = "{api_path}{account_id}/{detail}".format(
            api_path=self.api_path,
            account_id=account_id,
            detail="detail" if detailed else "")
        return self.connection.get_request(request_path)

    def set_name(self, account_id, name):
        """Set full name for account.

        :param account_id: (account_ID|username|email|name) as a string value
        :param name: Full name for account as a string
        :return: response as a dict {'name': Full Name}
        """

        data = {"name": name}
        request_path = "{api_path}{account_id}/name".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.put_request(request_path, data=data)

    def set_username(self, account_id, username):
        """Set the username of an account in Gerrit.

        Once set, the username cannot be changed or deleted.
        If attempted this fails with 405 - Method Not Allowed.
        :param account_id: (account_ID|username|email|name) as a string value
        :param username: Username of an account as a string
        :return: response username as a string
        """
        data = {"username": username}
        request_path = "{api_path}{account_id}/username".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.put_request(request_path, data=data)

    def is_active(self, account_id):
        """Check the status of an account in Gerrit."""

        request_path = "{api_path}{account_id}/active".format(
            api_path=self.api_path,
            account_id=account_id)
        result = self.connection.get_request(request_path)
        return True if result else False

    def enable(self, account_id):
        """Enable account in Gerrit."""

        request_path = "{api_path}{account_id}/active".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.put_request(request_path, data={})

    def disable(self, account_id):
        """Disable account in Gerrit."""

        request_path = "{api_path}{account_id}/active".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.delete_request(request_path, data={})

    def set_password(self, account_id, password=None, generate=False):
        """Set/Generate the HTTP password of an account in Gerrit.

        Only Gerrit administrators may set the HTTP password directly.
        If password is empty or not set and generate is False or not set,
        the HTTP password is deleted.

        :param account_id: (account_ID|username|email|name) as a string value
        :param password: password as a string
        :param generate: boolean value, if True then password will be generated
        :return: set/generated password as a string or
                 empty dict {} if password is deleted
        """

        data = {k: v for
                k, v in (('generate', generate),
                         ('http_password', password)) if v is not None}
        request_path = "{api_path}{account_id}/password.http".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.put_request(request_path, data=data)

    def delete_password(self, account_id):
        """Delete the HTTP password of an account in Gerrit."""

        request_path = "{api_path}{account_id}/password.http".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.delete_request(request_path, data={})

    def get_ssh_keys(self, account_id):
        """Get list of SSH keys of an account in Gerrit."""

        request_path = "{api_path}{account_id}/sshkeys".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.get_request(request_path)

    def get_ssh_key(self, account_id, sequence_id):
        """Retrieve an SSH key of a user.

        :param account_id: (account_ID|username|email|name) as a string value
        :param sequence_id: int value of a sequence number
        :return: dict that describes the SSH key
        """

        request_path = "{api_path}{account_id}/sshkeys/{sequence_id}".format(
            api_path=self.api_path,
            account_id=account_id,
            sequence_id=sequence_id)
        return self.connection.get_request(request_path)

    def add_ssh_key(self, account_id, ssh_key):
        """Add an SSH key for a user."""

        request_path = "{api_path}{account_id}/sshkeys".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.post_request(request_path, data=ssh_key,
                                            content_type='plain/text')

    def delete_ssh_key(self, account_id, ssh_key_id):
        """Delete an SSH key of a user."""

        request_path = "{api_path}{account_id}/sshkeys/{ssh_key_id}".format(
            api_path=self.api_path,
            account_id=account_id,
            ssh_key_id=ssh_key_id)
        return self.connection.delete_request(request_path)

    def get_membership(self, account_id):
        """Lists all groups that contain the specified user as a member."""

        request_path = "{api_path}{account_id}/groups".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.get_request(request_path)


def get_client(connection):
    return AccountClient(connection)
