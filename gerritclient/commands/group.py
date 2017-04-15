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

from gerritclient.commands import base
from gerritclient.common import utils


class GroupMixIn(object):

    entity_name = 'group'


class GroupList(GroupMixIn, base.BaseListCommand):
    """Lists all groups in Gerrit Code Review."""

    columns = ('group_id',
               'name',
               'id',
               'url',
               'options',
               'description',
               'owner',
               'owner_id')


class GroupShow(GroupMixIn, base.BaseShowCommand):
    """Shows information about specific group in Gerrit Code Review."""

    columns = ('group_id',
               'name',
               'id',
               'url',
               'options',
               'description',
               'owner',
               'owner_id')

    def get_parser(self, prog_name):
        parser = super(GroupShow, self).get_parser(prog_name)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Show more details about group.'
        )
        return parser

    def take_action(self, parsed_args):
        data = self.client.get_by_entity_id(parsed_args.entity_id,
                                            detailed=parsed_args.all)
        if parsed_args.all:
            self.columns += ('members', 'includes')
            # get only some fields from 'members' and 'includes' dicts
            # (in detailed mode) to make output more user friendly
            data['members'] = ', '.join([item['username'] +
                                         "(" + str(item['_account_id']) + ")"
                                         for item in data['members']])
            data['includes'] = ', '.join([item['name'] +
                                          "(" + str(item['group_id']) + ")"
                                          for item in data['includes']])
        data = utils.get_display_data_single(self.columns, data)
        return self.columns, data


class GroupMemberList(GroupMixIn, base.BaseListCommand):
    """Lists all members of specific group in Gerrit Code Review."""

    columns = ('_account_id',
               'username',
               'name',
               'email')

    def get_parser(self, app_name):
        parser = super(GroupMemberList, self).get_parser(app_name)

        parser.add_argument(
            'entity_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        parser.add_argument(
            '-a',
            '--all',
            action="store_true",
            help='Show members from included groups.'
        )

        return parser

    def take_action(self, parsed_args):
        data = self.client.get_group_members(parsed_args.entity_id,
                                             detailed=parsed_args.all)
        data = utils.get_display_data_multi(self.columns, data)

        return self.columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", GroupList, argv)


if __name__ == "__main__":
    debug()
