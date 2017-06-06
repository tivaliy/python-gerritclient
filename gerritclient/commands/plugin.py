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

import argparse
import os

from gerritclient.commands import base
from gerritclient.common import utils
from gerritclient import error


class PluginsMixIn(object):

    entity_name = 'plugin'


class PluginList(PluginsMixIn, base.BaseListCommand):
    """Lists all installed plugins in Gerrit Code Review."""

    columns = ('id',
               'name',
               'version',
               'index_url')

    def get_parser(self, app_name):
        parser = super(PluginList, self).get_parser(app_name)
        parser.add_argument(
            '-a',
            '--all',
            action="store_true",
            help='Show all plugins (including disabled).'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.all:
            self.columns += ('disabled',)
        data = self.client.get_all(detailed=parsed_args.all)
        data = self._reformat_data(data)
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
        return self.columns, data


class PluginShow(PluginsMixIn, base.BaseShowCommand):
    """Shows information about specific plugin in Gerrit Code Review."""

    columns = ('id',
               'version',
               'index_url',
               'disabled')


class PluginEnable(PluginsMixIn, base.BaseEntitySetState):
    """Enables a plugin on the Gerrit server."""

    action_type = 'enable'


class PluginDisable(PluginsMixIn, base.BaseEntitySetState):
    """Disables a plugin on the Gerrit server."""

    action_type = 'disable'


class PluginReload(PluginsMixIn, base.BaseShowCommand):
    """Reloads a plugin on the Gerrit server."""

    columns = ('id',
               'version',
               'index_url',
               'disabled')

    def take_action(self, parsed_args):
        response = self.client.reload(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class PluginInstall(PluginsMixIn, base.BaseShowCommand):
    """Installs a new plugin on the Gerrit server."""

    columns = ('id',
               'version',
               'index_url',
               'disabled')

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    def get_parser(self, app_name):
        parser = super(PluginInstall, self).get_parser(app_name)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--url',
            help='URL to the plugin jar.'
        )
        group.add_argument(
            '--file',
            type=self.get_file_path,
            help='File path to the plugin jar.'
        )
        return parser

    def take_action(self, parsed_args):
        if os.path.splitext(parsed_args.entity_id)[1] != '.jar':
            raise ValueError('Plugin identifier must contain ".jar" prefix')
        source_type, value = 'url', parsed_args.url
        if parsed_args.file:
            try:
                with open(parsed_args.file, 'rb') as stream:
                    source_type, value = 'file', stream.read()
            except (OSError, IOError):
                msg = "Could not read data from '{0}'".format(parsed_args.file)
                raise error.InvalidFileException(msg)
        response = self.client.install(parsed_args.entity_id,
                                       source_type=source_type,
                                       value=value)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", PluginList, argv)


if __name__ == "__main__":
    debug()
