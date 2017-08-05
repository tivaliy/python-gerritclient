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
import argparse
import six

from cliff import command
from cliff import lister
from cliff import show

from gerritclient import client
from gerritclient.common import utils
from gerritclient import error

VERSION = 'v1'


@six.add_metaclass(abc.ABCMeta)
class BaseCommand(command.Command):
    """Base Gerrit Code Review Client command."""

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.client = client.get_client(self.entity_name, VERSION)

    @abc.abstractproperty
    def entity_name(self):
        """Name of the Gerrit Code Review entity.

        :rtype: str
        """


@six.add_metaclass(abc.ABCMeta)
class BaseListCommand(lister.Lister, BaseCommand):
    """Lists all entities."""

    @property
    def default_sorting_by(self):
        """The first column in resulting table is default sorting field."""
        return [self.columns[0]]

    @abc.abstractproperty
    def columns(self):
        """Names of columns in the resulting table as a tuple."""
        pass

    @staticmethod
    def _reformat_data(data):
        """Reformat map of entities to list of respective entry values.

        As Gerrit returns a map that maps entity names to respective entries
        in all list commands, let's retrieve these entity name keys
        from received data, add it as a 'name'-key value to entry and return
        only values of respective entries as a list:
        {                               {
          "entity_name_1": {...},          "entity_name_1":
                ...                           {"name": "entity_name_1", ...},
                ...                --->                ...
                ...                                    ...
          "entity_name_n": {...}           "entity_name_n":
                                              {"name": "entity_name_n", ...}
        }                               }

        ---> [{"name": "entity_name_1", ...}, {"name": "entity_name_n", ...}]

        :param data: A map that maps entity names to respective entries
        :return:     List of dictionaries containing values of entries.
        """
        for entity_item in data:
            data[entity_item]['name'] = entity_item
        return data.values()

    def get_parser(self, prog_name):
        parser = super(BaseListCommand, self).get_parser(prog_name)

        # Add sorting key argument to the 'output formatters' group
        # (if exists), otherwise add it to the general group
        matching_groups = (group for group in parser._action_groups
                           if group.title == 'output formatters')

        group = next(matching_groups, None) or parser

        group.add_argument('-s',
                           '--sort-columns',
                           nargs='+',
                           choices=self.columns,
                           metavar='SORT_COLUMN',
                           default=self.default_sorting_by,
                           help="Space separated list of keys for sorting "
                                "the data. Defaults to '{}'. Wrong values "
                                "are ignored.".format(
                                    ', '.join(self.default_sorting_by)))
        return parser

    def take_action(self, parsed_args):
        data = self.client.get_all()
        data = self._reformat_data(data)
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data


@six.add_metaclass(abc.ABCMeta)
class BaseShowCommand(show.ShowOne, BaseCommand):
    """Shows detailed information about the entity."""

    @abc.abstractproperty
    def columns(self):
        """Names of columns in the resulting table."""
        pass

    def get_parser(self, app_name):
        parser = super(BaseShowCommand, self).get_parser(app_name)

        parser.add_argument(
            'entity_id',
            metavar='{0}-identifier'.format(self.entity_name),
            type=str,
            help='{0} identifier.'.format(self.entity_name.capitalize())
        )

        return parser

    def take_action(self, parsed_args):
        data = self.client.get_by_id(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, data)

        return self.columns, data


@six.add_metaclass(abc.ABCMeta)
class BaseCreateCommand(BaseShowCommand):
    """Creates entity."""

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    def get_parser(self, prog_name):
        parser = super(BaseCreateCommand, self).get_parser(prog_name)
        parser.add_argument(
            '--file',
            type=self.get_file_path,
            help='File with metadata to be uploaded.'
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            # If no additional data specified in the file,
            # then create a entity with default parameters
            data = utils.read_from_file(file_path) if file_path else None
        except (OSError, IOError):
            msg = "Could not read metadata for {0} '{1}' at {2}".format(
                self.entity_name, parsed_args.entity_id, file_path)
            raise error.InvalidFileException(msg)

        response = self.client.create(parsed_args.entity_id, data=data)
        response = utils.get_display_data_single(self.columns, response)
        self.app.stdout.write("{0} '{1}' was successfully created.\n".format(
            self.entity_name.capitalize(), parsed_args.entity_id))

        return self.columns, response


class BaseEntitySetState(BaseCommand):

    @abc.abstractproperty
    def action_type(self):
        """Type of action: ('enable'|'disable').

        :rtype: str
        """
        pass

    def get_parser(self, prog_name):
        parser = super(BaseEntitySetState, self).get_parser(prog_name)
        parser.add_argument(
            'entity_id',
            metavar='{0}-identifier'.format(self.entity_name),
            help='{0} identifier.'.format(self.entity_name.capitalize())
        )
        return parser

    def take_action(self, parsed_args):
        actions = {'enable': self.client.enable,
                   'disable': self.client.disable}
        actions[self.action_type](parsed_args.entity_id)
        msg = ("{0} with identifier '{1}' was successfully {2}d.\n".format(
            self.entity_name.capitalize(),
            parsed_args.entity_id,
            self.action_type))
        self.app.stdout.write(msg)
