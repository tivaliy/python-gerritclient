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

import abc

import six

from gerritclient.commands import base
from gerritclient.common import utils


class AccountMixIn(object):

    entity_name = 'account'


class AccountList(AccountMixIn, base.BaseListCommand):
    """Lists all accounts in Gerrit visible to the caller."""

    columns = ('_account_id',)

    def get_parser(self, app_name):
        parser = super(AccountList, self).get_parser(app_name)
        parser.add_argument(
            'query',
            help='Query string.'
        )
        parser.add_argument(
            '--suggest',
            action="store_true",
            help='Get account suggestions.'
        )
        parser.add_argument(
            '-l',
            '--limit',
            type=int,
            help='Limit the number of accounts to be included in the results.'
        )
        parser.add_argument(
            '-S',
            '--skip',
            type=int,
            help='Skip the given number of accounts '
                 'from the beginning of the list.'
        )
        parser.add_argument(
            '-a',
            '--all',
            action="store_true",
            help='Includes full name, preferred email, '
                 'username and avatars for each account.'
        )
        parser.add_argument(
            '--all-emails',
            action="store_true",
            help='Includes all registered emails.'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.all or parsed_args.suggest:
            self.columns += ('username', 'name', 'email')
        if parsed_args.all_emails and not parsed_args.all:
            self.columns += ('email', 'secondary_emails')
        if parsed_args.all_emails and parsed_args.all or parsed_args.suggest:
            self.columns += ('secondary_emails',)

        response = self.client.get_all(parsed_args.query,
                                       suggested=parsed_args.suggest,
                                       limit=parsed_args.limit,
                                       skip=parsed_args.skip,
                                       detailed=parsed_args.all,
                                       all_emails=parsed_args.all_emails)
        data = utils.get_display_data_multi(self.columns, response,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data


class AccountShow(AccountMixIn, base.BaseShowCommand):
    """Shows information about specific account in Gerrit."""

    columns = ('_account_id',
               'name',
               'email',
               'username')

    def get_parser(self, prog_name):
        parser = super(AccountShow, self).get_parser(prog_name)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Show more details about account.'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.all:
            self.columns += ('secondary_emails', 'registered_on')
        response = self.client.get_by_id(parsed_args.entity_id,
                                         detailed=parsed_args.all)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class AccountCreate(AccountMixIn, base.BaseCreateCommand):
    """Creates a new account in Gerrit Code Review."""

    columns = ('_account_id',
               'username',
               'name',
               'email')


@six.add_metaclass(abc.ABCMeta)
class BaseAccountSetCommand(AccountMixIn, base.BaseCommand):

    @abc.abstractmethod
    def action(self, account_id, attribute):
        pass

    @abc.abstractproperty
    def attribute(self):
        pass

    def get_parser(self, prog_name):
        parser = super(BaseAccountSetCommand, self).get_parser(prog_name)
        parser.add_argument(
            'account_id',
            metavar='account-identifier',
            help='Account identifier.'
        )
        parser.add_argument(
            'attribute',
            metavar='{attribute}'.format(attribute=self.attribute),
            help='Account {attribute}.'.format(attribute=self.attribute)
        )
        return parser

    def take_action(self, parsed_args):
        self.action(parsed_args.account_id, parsed_args.attribute)
        msg = ("{0} for the account with identifier '{1}' "
               "was successfully set.\n".format(self.attribute.capitalize(),
                                                parsed_args.account_id))
        self.app.stdout.write(msg)


class AccountSetName(BaseAccountSetCommand):
    """Sets the full name of an account in Gerrit Code Review."""

    attribute = "name"

    def action(self, account_id, attribute):
        return self.client.set_name(account_id, name=attribute)


class AccountSetUsername(BaseAccountSetCommand):
    """Sets the username of an account in Gerrit Code Review."""

    attribute = "username"

    def action(self, account_id, attribute):
        return self.client.set_username(account_id, username=attribute)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", AccountList, argv)


if __name__ == "__main__":
    debug()
