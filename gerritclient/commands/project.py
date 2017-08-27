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
            '-a',
            '--all',
            action='store_true',
            help='Include hidden projects in the results.'
        )
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
        data = self.client.get_all(is_all=parsed_args.all,
                                   limit=parsed_args.limit,
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
        data = self.client.get_by_name(parsed_args.entity_id)
        data = self._retrieve_web_links(data)
        data = utils.get_display_data_single(self.columns, data)

        return self.columns, data


class ProjectCreate(ProjectMixIn, base.BaseCreateCommand):
    """Creates a new project in Gerrit Code Review."""

    columns = ('id',
               'name',
               'parent',
               'description')


class ProjectDelete(ProjectMixIn, base.BaseCommand):
    """Deletes specified project from Gerrit Code Review.

    Note, 'deleteproject' plugin must be installed.
    """

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='Delete project even if it has open changes.'
        )
        parser.add_argument(
            '--preserve-git-repository',
            action='store_true',
            help='Do not delete git repository directory.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete(parsed_args.name,
                           force=parsed_args.force,
                           preserve=parsed_args.preserve_git_repository)
        msg = "Project '{0}' was deleted\n".format(parsed_args.name)
        self.app.stdout.write(msg)


class ProjectDescriptionShow(ProjectMixIn, base.BaseCommand):
    """Retrieves the description of a project."""

    def get_parser(self, prog_name):
        parser = super(ProjectDescriptionShow, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_description(parsed_args.name)
        self.app.stdout.write("{description}\n".format(description=response))


class ProjectDescriptionSet(ProjectMixIn, base.BaseCommand):
    """Retrieves the description of a project."""

    def get_parser(self, prog_name):
        parser = super(ProjectDescriptionSet, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        parser.add_argument(
            '-d',
            '--description',
            help='The project description. The project '
                 'description will be deleted if not set.'
        )
        parser.add_argument(
            '-m',
            '--message',
            help='Message that should be used to commit the change '
                 'of the project description in the project.config file '
                 'to the refs/meta/config branch.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_description(
            parsed_args.name,
            description=parsed_args.description,
            commit_message=parsed_args.message
        )
        msg = "The description for the project '{0}' was {1}\n".format(
            parsed_args.name,
            'set: {}'.format(response) if response else 'deleted.')
        self.app.stdout.write(msg)


class ProjectParentShow(ProjectMixIn, base.BaseCommand):
    """Retrieves the name of a project\'s parent project."""

    def get_parser(self, prog_name):
        parser = super(ProjectParentShow, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_parent(parsed_args.name)
        self.app.stdout.write('{0}\n'.format(response))


class ProjectParentSet(ProjectMixIn, base.BaseCommand):
    """Sets the parent project for a project."""

    def get_parser(self, prog_name):
        parser = super(ProjectParentSet, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        parser.add_argument(
            '-p',
            '--parent',
            required=True,
            help='The name of the parent project.'
        )
        parser.add_argument(
            '-m',
            '--message',
            help='Message that should be used to commit the change '
                 'of the project parent in the project.config file '
                 'to the refs/meta/config branch.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_parent(parsed_args.name,
                                          parent=parsed_args.parent,
                                          commit_message=parsed_args.message)
        self.app.stdout.write("A new parent project '{0}' was set for project "
                              "'{1}'.\n".format(response, parsed_args.name))


class ProjectHeadShow(ProjectMixIn, base.BaseCommand):
    """Retrieves for a project the name of the branch to which HEAD points."""

    def get_parser(self, prog_name):
        parser = super(ProjectHeadShow, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_head(parsed_args.name)
        self.app.stdout.write('{0}\n'.format(response))


class ProjectHeadSet(ProjectMixIn, base.BaseCommand):
    """Sets HEAD for a project."""

    def get_parser(self, prog_name):
        parser = super(ProjectHeadSet, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        parser.add_argument(
            '-b',
            '--branch',
            required=True,
            help='The name of the branch to which HEAD should point.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_head(parsed_args.name,
                                        branch=parsed_args.branch)
        msg = ("HEAD for the project '{0}' was set "
               "to the branch '{1}'\n".format(parsed_args.name, response))
        self.app.stdout.write(msg)


class ProjectRepoStatisticsShow(ProjectMixIn, base.BaseShowCommand):
    """Return statistics for the repository of a project."""

    columns = ('number_of_loose_objects',
               'number_of_loose_refs',
               'number_of_pack_files',
               'number_of_packed_objects',
               'number_of_packed_refs',
               'size_of_loose_objects',
               'size_of_packed_objects')

    def take_action(self, parsed_args):
        response = self.client.get_repo_statistics(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ProjectBranchList(ProjectMixIn, base.BaseListCommand):
    """Lists the branches of a project."""

    columns = ('ref',
               'revision',
               'can_delete',
               'web_links')

    def get_parser(self, prog_name):
        parser = super(ProjectBranchList, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_branches(parsed_args.name)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ProjectBranchShow(ProjectMixIn, base.BaseShowCommand):
    """Retrieves a branch of a project."""

    columns = ('ref',
               'revision',
               'can_delete',
               'web_links')

    def get_parser(self, app_name):
        parser = super(ProjectBranchShow, self).get_parser(app_name)
        parser.add_argument(
            '-b',
            '--branch',
            required=True,
            help='The name of a branch or HEAD. '
                 'The prefix refs/heads/ can be omitted.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_branch(parsed_args.entity_id,
                                          branch_name=parsed_args.branch)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ProjectBranchCreate(ProjectMixIn, base.BaseShowCommand):
    """Creates a new branch."""

    columns = ('ref',
               'revision',
               'can_delete',
               'web_links')

    def get_parser(self, app_name):
        parser = super(ProjectBranchCreate, self).get_parser(app_name)
        parser.add_argument(
            '-b',
            '--branch',
            required=True,
            help='The name of a branch or HEAD. '
                 'The prefix refs/heads/ can be omitted.'
        )
        parser.add_argument(
            '-r',
            '--revision',
            help='The base revision of the new branch. '
                 'If not set, HEAD will be used as base revision.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.create_branch(parsed_args.entity_id,
                                             branch_name=parsed_args.branch,
                                             revision=parsed_args.revision)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ProjectBranchDelete(ProjectMixIn, base.BaseCommand):
    """Deletes one or more branches."""

    def get_parser(self, prog_name):
        parser = super(ProjectBranchDelete, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of project.'
        )
        parser.add_argument(
            '-b',
            '--branch',
            nargs='+',
            required=True,
            help='The branches that should be deleted.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_branch(parsed_args.name, parsed_args.branch)
        msg = ("The following branches of the project '{0}' were deleted: {1}."
               "\n".format(parsed_args.name, ', '.join(parsed_args.branch)))
        self.app.stdout.write(msg)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", ProjectList, argv)


if __name__ == "__main__":
    debug()
