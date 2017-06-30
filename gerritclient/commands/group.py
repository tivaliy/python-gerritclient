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
        data = self.client.get_by_id(parsed_args.entity_id,
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


class GroupCreate(GroupMixIn, base.BaseCreateCommand):
    """Creates a new group in Gerrit Code Review."""

    columns = ('group_id',
               'name',
               'options',
               'description',
               'owner')


class GroupRename(GroupMixIn, base.BaseCommand):
    """Renames a Gerrit internal group."""

    def get_parser(self, prog_name):
        parser = super(GroupRename, self).get_parser(prog_name)
        parser.add_argument(
            'group_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        parser.add_argument(
            'new_name',
            help='New group name.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.rename(parsed_args.group_id,
                                      parsed_args.new_name)
        msg = ("Group with identifier '{0}' was successfully renamed to "
               "'{1}'.\n".format(parsed_args.group_id, response))
        self.app.stdout.write(msg)


class GroupSetDescription(GroupMixIn, base.BaseCommand):
    """Sets the description of a specified Gerrit internal group."""

    def get_parser(self, prog_name):
        parser = super(GroupSetDescription, self).get_parser(prog_name)
        parser.add_argument(
            'group_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        parser.add_argument(
            'description',
            help='Group description.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.set_description(parsed_args.group_id,
                                    parsed_args.description)
        msg = ("Description for the group with identifier '{0}' "
               "was successfully set.\n".format(parsed_args.group_id))
        self.app.stdout.write(msg)


class GroupDeleteDescription(GroupMixIn, base.BaseCommand):
    """Deletes the description of a specified Gerrit internal group."""

    def get_parser(self, prog_name):
        parser = super(GroupDeleteDescription, self).get_parser(prog_name)
        parser.add_argument(
            'group_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_description(parsed_args.group_id)
        msg = ("Description for the group with identifier '{0}' "
               "was successfully removed.\n".format(parsed_args.group_id))
        self.app.stdout.write(msg)


class GroupSetOptions(GroupMixIn, base.BaseShowCommand):
    """Sets the options of a Gerrit internal group."""

    columns = ('visible_to_all',)

    def get_parser(self, prog_name):
        parser = super(GroupSetOptions, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--visible',
            dest='visibility',
            action='store_true',
            help="Set group visible to all registered users."
        )
        group.add_argument(
            '--no-visible',
            dest='visibility',
            action='store_false',
            help="Set group not visible to all registered users."
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_options(parsed_args.entity_id,
                                           parsed_args.visibility)
        msg = ("The group with identifier '{0}' was successfully updated "
               "with the following options:\n".format(parsed_args.entity_id))
        self.app.stdout.write(msg)
        data = utils.get_display_data_single(self.columns, response)

        return self.columns, data


class GroupSetOwner(GroupMixIn, base.BaseCommand):
    """Sets the owner group of a Gerrit internal group."""

    def get_parser(self, prog_name):
        parser = super(GroupSetOwner, self).get_parser(prog_name)
        parser.add_argument(
            'group_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        parser.add_argument(
            'owner',
            help='Group owner.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_owner_group(parsed_args.group_id,
                                               parsed_args.owner)
        msg = ("Owner group '{0}' with id '{1}' was successfully assigned to "
               "the group with id '{2}':\n".format(response['name'],
                                                   response['group_id'],
                                                   parsed_args.group_id))
        self.app.stdout.write(msg)


class GroupMemberList(GroupMixIn, base.BaseListCommand):
    """Lists all members of specific group in Gerrit Code Review."""

    columns = ('_account_id',
               'username',
               'name',
               'email')

    def get_parser(self, app_name):
        parser = super(GroupMemberList, self).get_parser(app_name)

        parser.add_argument(
            'group_id',
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
        data = self.client.get_members(parsed_args.group_id,
                                       detailed=parsed_args.all)
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data


@six.add_metaclass(abc.ABCMeta)
class BaseGroupAction(GroupMixIn, base.BaseCommand):

    @abc.abstractproperty
    def action(self):
        """Type of action: ('add'|'delete'|'include'|'exclude').

        :rtype: str
        """
        pass

    @abc.abstractproperty
    def attribute(self):
        """Type of attribute: ('account'|'group')

        :return: str
        """
        pass

    def get_parser(self, app_name):
        parser = super(BaseGroupAction, self).get_parser(app_name)
        parser.add_argument(
            'group_id',
            metavar='group-identifier',
            help='Group identifier.'
        )
        parser.add_argument(
            '--{attribute}'.format(attribute=self.attribute),
            required=True,
            nargs='+',
            metavar='{}-identifier'.format(self.attribute),
            help='{}(s) identifier(s).'.format(self.attribute.capitalize())
        )
        return parser

    def take_action(self, parsed_args):
        actions = {'add': self.client.add_members,
                   'delete': self.client.delete_members,
                   'include': self.client.include,
                   'exclude': self.client.exclude}
        ids = parsed_args.__getattribute__(self.attribute)
        actions[self.action](parsed_args.group_id, ids)
        msg = ("The following {}s were successfully {}(e)d to/from the "
               "group with ID='{}': {}.\n".format(self.attribute,
                                                  self.action,
                                                  parsed_args.group_id,
                                                  ', '.join(ids)))
        self.app.stdout.write(msg)


class GroupMemberAdd(BaseGroupAction):
    """Adds a user or several users as member(s) to a Gerrit internal group."""

    action = 'add'

    attribute = 'account'


class GroupMemberDelete(BaseGroupAction):
    """Removes a user or several users from a Gerrit internal group."""

    action = 'delete'

    attribute = 'account'


class GroupInclude(BaseGroupAction):
    """Includes one or several groups into a Gerrit internal group."""

    action = 'include'

    attribute = 'group'


class GroupExclude(BaseGroupAction):
    """Deletes one or several included groups from a Gerrit internal group."""

    action = 'exclude'

    attribute = 'group'


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", GroupList, argv)


if __name__ == "__main__":
    debug()
