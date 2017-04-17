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

from cliff import command
from cliff import lister
from cliff import show

from gerritclient import client
from gerritclient.common import utils

VERSION = 'v1'


@six.add_metaclass(abc.ABCMeta)
class BaseCommand(command.Command):
    """Base Gerrit Code Review Client command."""

    def __init__(self, *args, **kwargs):
        super(BaseCommand, self).__init__(*args, **kwargs)
        self.client = client.get_client(self.entity_name, VERSION)

    @abc.abstractproperty
    def entity_name(self):
        """Name of the Gerrit Code Review entity."""


@six.add_metaclass(abc.ABCMeta)
class BaseListCommand(lister.Lister, BaseCommand):
    """Lists all entities."""

    @abc.abstractproperty
    def columns(self):
        """Names of columns in the resulting table."""
        pass

    def _reformat_data(self, data):
        # As Gerrit returns a map that maps entity names to respective entries
        # in all list commands, let's retrieve these entity name keys
        # from received data and add it as a 'name'-key value to entry:
        # {                               {
        #   "entity_name_1": {...},          "entity_name_1":
        #         ...                           {"name": "entity_name_1", ...},
        #         ...               ---->                ...
        #         ...                                    ...
        #   "entity_name_n": {...}           "entity_name_n":
        #                                       {"name": "entity_name_n", ...}
        # }                               }
        for entity_item in data:
            data[entity_item]['name'] = entity_item
        data = utils.get_display_data_multi(self.columns, data.values())
        return data

    def take_action(self, parsed_args):
        data = self.client.get_all()

        return self.columns, self._reformat_data(data)


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
        data = self.client.get_by_entity_id(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, data)

        return self.columns, data
