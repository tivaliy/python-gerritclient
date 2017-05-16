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

    def get_by_id(self, account_id):
        """Get data about specific account in Gerrit.

        :param account_id: (account_ID|username|email|name) as a string value
        :return: dict, that contains information about account
        """

        request_path = "{api_path}{account_id}".format(
            api_path=self.api_path,
            account_id=account_id)
        return self.connection.get_request(request_path)


def get_client(connection):
    return AccountClient(connection)
