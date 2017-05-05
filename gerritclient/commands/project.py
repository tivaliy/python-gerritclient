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

from gerritclient.commands import base
from gerritclient.common import utils
from gerritclient import error


class ProjectMixIn(object):
    entity_name = 'project'

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(
                'File "{0}" does not exist'.format(file_path))
        return file_path

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
        parser.add_argument(
            '-l',
            '--limit',
            type=int,
            help='Limit the number of projects to be included in the results.'
        )
        parser.add_argument(
            '-S',
            '--skip',
            type=int,
            help='Skip the given number of projects '
                 'from the beginning of the list.'
        )
        parser.add_argument(
            '--type',
            choices=['code', 'permissions', 'all'],
            help='Display only projects of the specified type.'
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-p',
            '--prefix',
            help='Limit the results to those projects '
                 'that start with the specified prefix.'
        )
        group.add_argument(
            '-m',
            '--match',
            help='Limit the results to those projects '
                 'that match the specified substring.'
        )
        group.add_argument(
            '-r',
            '--regex',
            help='Limit the results to those projects '
                 'that match the specified regex.'
        )
        return parser

    def take_action(self, parsed_args):
        if parsed_args.description:
            self.columns += ('description',)
        if parsed_args.branches:
            self.columns += ('branches',)
        fetch_pattern = {k: v for k, v in (('prefix', parsed_args.prefix),
                                           ('match', parsed_args.match),
                                           ('regex', parsed_args.regex))
                         if v is not None}
        fetch_pattern = fetch_pattern if fetch_pattern else None
        data = self.client.get_all(limit=parsed_args.limit,
                                   skip=parsed_args.skip,
                                   pattern_dispatcher=fetch_pattern,
                                   project_type=parsed_args.type,
                                   description=parsed_args.description,
                                   branches=parsed_args.branches)
        data = self._reformat_data(data)
        for item in data:
            item = self._retrieve_web_links(item)
            if parsed_args.branches:
                item['branches'] = self._retrieve_branches(item)
        data = utils.get_display_data_multi(self.columns, data,
                                            sort_by=parsed_args.sort_columns)
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


class ProjectCreate(ProjectMixIn, base.BaseShowCommand):
    """Creates a new project in Gerrit Code Review."""

    columns = ('id',
               'name',
               'parent',
               'description')

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument(
            '--file',
            type=self.get_file_path,
            help='File with data to be uploaded.'
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            # If no additional data specified in file,
            # then create a project with default parameters
            data = utils.read_from_file(file_path) if file_path else None
        except (OSError, IOError):
            msg = "Could not read metadata for project '{}' at {}".format(
                parsed_args.entity_id, file_path)
            raise error.InvalidFileException(msg)

        response = self.client.create(parsed_args.entity_id, data=data)
        response = utils.get_display_data_single(self.columns, response)
        self.app.stdout.write("Project '{0}' was successfully "
                              "created.\n".format(parsed_args.entity_id))

        return self.columns, response


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", ProjectList, argv)


if __name__ == "__main__":
    debug()
