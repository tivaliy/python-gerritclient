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

        return self.columns, self._reformat_data(data)


class PluginShow(PluginsMixIn, base.BaseShowCommand):
    """Shows information about specific plugin in Gerrit Code Review."""

    columns = ('id',
               'version',
               'index_url',
               'disabled')


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", PluginList, argv)


if __name__ == "__main__":
    debug()
