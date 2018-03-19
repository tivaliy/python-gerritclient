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
        data = utils.get_display_data_multi(self.columns, data)
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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
            help='Name of the project.'
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


class ProjectBranchReflogShow(ProjectMixIn, base.BaseListCommand):
    """Gets the reflog of a certain branch.

    The caller must be project owner.
    """

    columns = ('old_id',
               'new_id',
               'who',
               'comment')

    def get_parser(self, prog_name):
        parser = super(ProjectBranchReflogShow, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '-b',
            '--branch',
            required=True,
            help='The name of a branch or HEAD. '
                 'The prefix refs/heads/ can be omitted.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_reflog(parsed_args.name,
                                          branch=parsed_args.branch)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ProjectChildList(ProjectMixIn, base.BaseListCommand):
    """Lists the direct child projects of a project.

    Child projects that are not visible to the calling user are ignored
    and are not resolved further.
    """

    columns = ('id',
               'name',
               'parent',
               'description')

    def get_parser(self, prog_name):
        parser = super(ProjectChildList, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '-r',
            '--recursively',
            action='store_true',
            help='Resolve the child projects of a project recursively.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_children(
            parsed_args.name, recursively=parsed_args.recursively)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ProjectGCRun(ProjectMixIn, base.BaseCommand):
    """Runs the Git garbage collection for the repository of a project.

    In case of asynchronous execution the --show-progress option is ignored.
    """

    def get_parser(self, prog_name):
        parser = super(ProjectGCRun, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '--show-progress',
            action='store_true',
            help='Show progress information.'
        )
        parser.add_argument(
            '--aggressive',
            action='store_true',
            help='Do aggressive garbage collection.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.run_gc(parsed_args.name,
                                      aggressive=parsed_args.aggressive,
                                      show_progress=parsed_args.show_progress)
        self.app.stdout.write(response)


class ProjectTagList(ProjectMixIn, base.BaseListCommand):
    """Lists the tags of a project.

    Only includes tags under the refs/tags/ namespace.
    """

    columns = ('ref',
               'revision',
               'object',
               'message',
               'tagger',
               'can_delete',
               'web_links')

    def get_parser(self, prog_name):
        parser = super(ProjectTagList, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '-l',
            '--limit',
            type=int,
            help='Limit the number of tags to be included in the results.'
        )
        parser.add_argument(
            '-S',
            '--skip',
            type=int,
            help='Skip the given number of tags '
                 'from the beginning of the list.'
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '-m',
            '--match',
            help='Limit the results to those tags that match the '
                 'specified substring. The match is case insensitive.'
        )
        group.add_argument(
            '-r',
            '--regex',
            help='Limit the results to those tags that match the '
                 'specified regex. The match is case sensitive.'
        )
        return parser

    def take_action(self, parsed_args):
        fetched_pattern = {k: v for k, v in (('match', parsed_args.match),
                                             ('regex', parsed_args.regex))
                           if v is not None} or None
        response = self.client.get_tags(parsed_args.name,
                                        limit=parsed_args.limit,
                                        skip=parsed_args.skip,
                                        pattern_dispatcher=fetched_pattern)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ProjectTagShow(ProjectMixIn, base.BaseShowCommand):
    """Retrieves a tag of a project."""

    columns = ('ref',
               'revision',
               'object',
               'message',
               'tagger',
               'can_delete',
               'web_links')

    def get_parser(self, prog_name):
        parser = super(ProjectTagShow, self).get_parser(prog_name)
        parser.add_argument(
            'tag',
            help='Name of the tag.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_tag(parsed_args.entity_id, parsed_args.tag)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ProjectTagCreate(ProjectMixIn, base.BaseShowCommand):
    """Creates a new tag on the project.

    If a message is provided in the input, the tag is created as an annotated
    tag with the current user as tagger. Signed tags are not supported.
    """

    columns = ('ref',
               'revision',
               'object',
               'message',
               'tagger',
               'can_delete',
               'web_links')

    def get_parser(self, prog_name):
        parser = super(ProjectTagCreate, self).get_parser(prog_name)
        parser.add_argument(
            '-t', '--tag',
            required=True,
            help='The name of the tag. The leading refs/tags/ is optional.'
        )
        parser.add_argument(
            '-r', '--revision',
            help="The revision to which the tag should point. "
                 "If not specified, the project's HEAD will be used."
        )
        parser.add_argument(
            '-m', '--message',
            help='The tag message. When set, the tag '
                 'will be created as an annotated tag.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.create_tag(parsed_args.entity_id,
                                          parsed_args.tag,
                                          revision=parsed_args.revision,
                                          message=parsed_args.message)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ProjectTagDelete(ProjectMixIn, base.BaseCommand):
    """Deletes one or more tags of the project."""

    def get_parser(self, prog_name):
        parser = super(ProjectTagDelete, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '-t',
            '--tag',
            nargs='+',
            required=True,
            help='The tags to be deleted.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_tag(parsed_args.name, parsed_args.tag)
        msg = ("The following tags of the project '{0}' were deleted: {1}."
               "\n".format(parsed_args.name, ', '.join(parsed_args.tag)))
        self.app.stdout.write(msg)


class ProjectConfigDownload(ProjectMixIn, base.BaseDownloadCommand):
    """Gets some configuration information about a project.

    Note that this config info is not simply the contents of project.config;
    it generally contains fields that may have been inherited from parent
    projects.
    """

    def get_parser(self, prog_name):
        parser = super(ProjectConfigDownload, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        return parser

    def take_action(self, parsed_args):
        file_name = '{}.{}'.format(utils.normalize(parsed_args.name),
                                   parsed_args.format)
        file_path = os.path.join(os.path.abspath(parsed_args.directory),
                                 file_name)
        response_data = self.client.get_config(parsed_args.name)
        try:
            if not os.path.exists(parsed_args.directory):
                os.makedirs(parsed_args.directory)
            with open(file_path, 'w') as stream:
                utils.safe_dump(parsed_args.format, stream, response_data)
        except (OSError, IOError) as e:
            msg = ("Could not store {0} data at {1}. "
                   "{2}".format(self.entity_name, file_path, e))
            raise error.InvalidFileException(msg)
        msg = "Information about the {} was stored in '{}' file.\n".format(
            self.entity_name, file_path)
        self.app.stdout.write(msg)


class ProjectConfigSet(ProjectMixIn, base.BaseCommand):
    """Sets the configuration of a project."""

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    def get_parser(self, prog_name):
        parser = super(ProjectConfigSet, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            help='Name of the project.'
        )
        parser.add_argument(
            '--file',
            type=self.get_file_path,
            required=True,
            help='File with metadata to be uploaded.'
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            data = utils.read_from_file(file_path)
        except (OSError, IOError):
            msg = ("Could not read configuration metadata for the project "
                   "'{0}' at {1}".format(parsed_args.name, file_path))
            raise error.InvalidFileException(msg)

        self.client.set_config(parsed_args.name, data=data)
        msg = ("Configuration of the project '{0}' was successfully "
               "updated.\n".format(parsed_args.name))
        self.app.stdout.write(msg)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", ProjectList, argv)


if __name__ == "__main__":
    debug()
