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


class ProjectMixIn(object):

    entity_name = 'project'

    @staticmethod
    def _retrieve_web_links(data):
        """Get 'web_links' dictionary from data and format it as a string."""

        if 'web_links' in data:
            data['web_links'] = ''.join(["{0} ({1})".format(
                item['name'], item['url']) for item in data['web_links']])
        return data


class ProjectList(ProjectMixIn, base.BaseListCommand):
    """Lists all projects accessible by the caller."""

    columns = ('name',
               'id',
               'state',
               'web_links')

    @staticmethod
    def _retrieve_branches(data):
        return ''.join('{0} ({1}); '.format(k, v)
                       for k, v in data['branches'].items())

    def get_parser(self, prog_name):
        parser = super(ProjectList, self).get_parser(prog_name)
        parser.add_argument(
            '-d',
            '--description',
            action='store_true',
            help='Include project description in the results.'
        )
        parser.add_argument(
            '-b',
            '--branches',
            nargs='+',
            default=None,
            help='Limit the results to the projects '
                 'having the specified branches and include the sha1 '
                 'of the branches in the results.'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.description:
            self.columns += ('description',)
        if parsed_args.branches:
            self.columns += ('branches',)
        data = self.client.get_all(description=parsed_args.description,
                                   branches=parsed_args.branches)
        for entity_item in data:
            data[entity_item]['name'] = entity_item
            data[entity_item] = self._retrieve_web_links(data[entity_item])
            if parsed_args.branches:
                data[entity_item]['branches'] = self._retrieve_branches(
                    data[entity_item])
        data = utils.get_display_data_multi(self.columns, data.values())

        return self.columns, data


class ProjectShow(ProjectMixIn, base.BaseShowCommand):
    """Shows information about specific project in Gerrit Code Review."""

    columns = ('id',
               'name',
               'parent',
               'description',
               'state',
               'web_links')

    def take_action(self, parsed_args):
        data = self.client.get_by_entity_id(parsed_args.entity_id)
        data = self._retrieve_web_links(data)
        data = utils.get_display_data_single(self.columns, data)

        return self.columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", ProjectList, argv)


if __name__ == "__main__":
    debug()
