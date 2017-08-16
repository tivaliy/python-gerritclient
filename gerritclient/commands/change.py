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

from gerritclient.commands import base
from gerritclient.common import utils
from gerritclient import error


class ChangeMixIn(object):

    entity_name = 'change'

    columns = ('id', 'project', 'branch', 'topic', 'hashtags', 'change_id',
               'subject', 'status', 'created', 'updated', 'submitted',
               'starred', 'stars', 'reviewed', 'submit_type', 'mergeable',
               'submittable', 'insertions', 'deletions',
               'unresolved_comment_count', '_number', 'owner', 'actions',
               'labels', 'permitted_labels', 'removable_reviewers',
               'reviewers', 'reviewer_updates', 'messages', 'current_revision',
               'revisions', '_more_changes', 'problems')


class ChangeCommentMixIn(object):

    entity_name = 'change'

    columns = ('patch_set', 'id', 'path', 'side', 'parent', 'line', 'range',
               'in_reply_to', 'message', 'updated', 'author', 'tag',
               'unresolved', 'robot_id', 'robot_run_id', 'url', 'properties',
               'fix_suggestions')

    @staticmethod
    def format_data(data):
        fetched_data = []
        for file_path, comment_info in data.items():
            for item in comment_info:
                item['path'] = file_path
                fetched_data.append(item)
        return fetched_data


class ChangeList(ChangeMixIn, base.BaseListCommand):
    """Queries changes visible to the caller. """

    def get_parser(self, prog_name):
        parser = super(ChangeList, self).get_parser(prog_name)
        parser.add_argument(
            'query',
            nargs='+',
            help='Query string.'
        )
        parser.add_argument(
            '-l',
            '--limit',
            type=int,
            help='Limit the number of changes to be included in the results.'
        )
        parser.add_argument(
            '-S',
            '--skip',
            type=int,
            help='Skip the given number of changes '
                 'from the beginning of the list.'
        )
        parser.add_argument(
            '-o',
            '--option',
            nargs='+',
            help='Fetch additional data about changes.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_all(query=parsed_args.query,
                                       options=parsed_args.option,
                                       limit=parsed_args.limit,
                                       skip=parsed_args.skip)
        # Clients are allowed to specify more than one query. In this case
        # the result is an array of arrays, one per query in the same order
        # the queries were given in. If the number of queries more then one,
        # then merge arrays in a single one to display data correctly.
        if len(parsed_args.query) > 1:
            response = [item for sublist in response for item in sublist]
        fetched_columns = [c for c in self.columns
                           if response and c in response[0]]
        data = utils.get_display_data_multi(fetched_columns, response)
        return fetched_columns, data


class ChangeShow(ChangeMixIn, base.BaseShowCommand):
    """Retrieves a change."""

    def get_parser(self, app_name):
        parser = super(ChangeShow, self).get_parser(app_name)
        parser.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='Retrieves a change with labels, detailed labels, '
                 'detailed accounts, reviewer updates, and messages.'
        )
        parser.add_argument(
            '-o',
            '--option',
            nargs='+',
            help='Fetch additional data about a change.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_by_id(change_id=parsed_args.entity_id,
                                         detailed=parsed_args.all,
                                         options=parsed_args.option)
        # As the number of columns can greatly very depending on request
        # let's fetch only those that are in response and print them in
        # respective (declarative) order
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeCreate(ChangeMixIn, base.BaseCommand, base.show.ShowOne):
    """Creates a new change."""

    columns = ('id', 'project', 'branch', 'topic', 'change_id', 'subject',
               'status', 'created', 'updated', 'mergeable', 'insertions',
               'deletions', '_number', 'owner')

    @staticmethod
    def get_file_path(file_path):
        if not utils.file_exists(file_path):
            raise argparse.ArgumentTypeError(
                "File '{0}' does not exist".format(file_path))
        return file_path

    def get_parser(self, prog_name):
        parser = super(ChangeCreate, self).get_parser(prog_name)
        parser.add_argument(
            'file',
            type=self.get_file_path,
            help='File with metadata of a new change.'
        )
        return parser

    def take_action(self, parsed_args):
        file_path = parsed_args.file
        try:
            data = utils.read_from_file(file_path)
        except (OSError, IOError):
            msg = "Could not read metadata at {0}".format(file_path)
            raise error.InvalidFileException(msg)

        response = self.client.create(data)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


@six.add_metaclass(abc.ABCMeta)
class BaseChangeAction(ChangeMixIn, base.BaseShowCommand):
    """Base class to perform actions on changes."""

    @property
    def parameters(self):
        """Additional parameters to be passed to 'action' method as a tuple."""

        return ()

    @abc.abstractmethod
    def action(self, change_id, **kwargs):
        pass

    def take_action(self, parsed_args):
        # Retrieve necessary parameters from argparse.Namespace object
        params = {k: v for
                  k, v in vars(parsed_args).items() if k in self.parameters}
        response = self.action(parsed_args.entity_id, **params)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeAbandon(BaseChangeAction):
    """Abandons a change."""

    def action(self, change_id, **kwargs):
        return self.client.abandon(change_id)


class ChangeRestore(BaseChangeAction):
    """Restores a change."""

    def action(self, change_id, **kwargs):
        return self.client.restore(change_id)


class ChangeRevert(BaseChangeAction):
    """Reverts a change."""

    parameters = ('message',)

    def get_parser(self, app_name):
        parser = super(ChangeRevert, self).get_parser(app_name)
        parser.add_argument(
            '-m',
            '--message',
            help='Message to be added as review '
                 'comment when reverting the change.'
        )
        return parser

    def action(self, change_id, message=None):
        return self.client.revert(change_id, message=message)


class ChangeMove(BaseChangeAction):
    """Moves a change."""

    parameters = ('branch', 'message')

    def get_parser(self, app_name):
        parser = super(ChangeMove, self).get_parser(app_name)
        parser.add_argument(
            '-b',
            '--branch',
            required=True,
            help='Destination branch.'
        )
        parser.add_argument(
            '-m',
            '--message',
            help="A message to be posted in this change's comments."
        )
        return parser

    def action(self, change_id, branch=None, message=None):
        return self.client.move(change_id, branch, message=message)


class ChangeSubmit(BaseChangeAction):
    """Submits a change."""

    parameters = ('on_behalf_of', 'notify')

    def get_parser(self, app_name):
        parser = super(ChangeSubmit, self).get_parser(app_name)
        parser.add_argument(
            '--on-behalf-of',
            help='Submit the change on behalf of the given user.'
        )
        parser.add_argument(
            '--notify',
            choices=['NONE', 'OWNER', 'OWNER_REVIEWERS', 'ALL'],
            default='ALL',
            help='Notify handling that defines to whom email notifications '
                 'should be sent after the change is submitted.'
        )
        return parser

    def action(self, change_id, on_behalf_of=None, notify=None):
        return self.client.submit(change_id,
                                  on_behalf_of=on_behalf_of,
                                  notify=notify)


class ChangeRebase(BaseChangeAction):
    """Rebases a change."""

    parameters = ('parent',)

    def get_parser(self, app_name):
        parser = super(ChangeRebase, self).get_parser(app_name)
        parser.add_argument(
            '-p',
            '--parent',
            help='The new parent revision.'
        )
        return parser

    def action(self, change_id, parent=None):
        return self.client.rebase(change_id, parent=parent)


class ChangeDelete(ChangeMixIn, base.BaseCommand):
    """Deletes a change."""

    def get_parser(self, prog_name):
        parser = super(ChangeDelete, self).get_parser(prog_name)
        parser.add_argument(
            'change_id',
            metavar='change-identifier',
            help='Change identifier.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete(parsed_args.change_id)
        self.app.stdout.write("Change with ID {0} was successfully "
                              "deleted.\n".format(parsed_args.change_id))


class ChangeTopicShow(ChangeMixIn, base.BaseShowCommand):
    """Retrieves the topic of a change."""

    columns = ('topic',)

    def take_action(self, parsed_args):
        response = self.client.get_topic(parsed_args.entity_id) or None
        data = utils.get_display_data_single(self.columns, {'topic': response})
        return self.columns, data


class ChangeTopicSet(ChangeMixIn, base.BaseShowCommand):
    """Sets the topic of a change."""

    columns = ('topic',)

    def get_parser(self, app_name):
        parser = super(ChangeTopicSet, self).get_parser(app_name)
        parser.add_argument(
            '-t',
            '--topic',
            required=True,
            help='Topic of a change.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_topic(parsed_args.entity_id,
                                         parsed_args.topic) or None
        data = utils.get_display_data_single(self.columns, {'topic': response})
        return self.columns, data


class ChangeTopicDelete(ChangeMixIn, base.BaseShowCommand):
    """Deletes the topic of a change."""

    columns = ('topic',)

    def take_action(self, parsed_args):
        response = self.client.delete_topic(parsed_args.entity_id) or None
        data = utils.get_display_data_single(self.columns, {'topic': response})
        return self.columns, data


class ChangeAssigneeShow(BaseChangeAction):
    """Retrieves the account of the user assigned to a change."""

    columns = ('_account_id',
               'name',
               'email',
               'username')

    def action(self, change_id, **kwargs):
        return self.client.get_assignee(change_id)


class ChangeAssigneeHistoryShow(ChangeMixIn, base.BaseListCommand):
    """Retrieve a list of every user ever assigned to a change."""

    columns = ('_account_id',
               'name',
               'email',
               'username')

    def get_parser(self, prog_name):
        parser = super(ChangeAssigneeHistoryShow, self).get_parser(prog_name)
        parser.add_argument(
            'change_id',
            metavar='change-identifier',
            help='Change identifier.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_assignees(parsed_args.change_id)
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ChangeAssigneeSet(ChangeMixIn, base.BaseShowCommand):
    """Sets the assignee of a change."""

    columns = ('_account_id',
               'name',
               'email',
               'username')

    def get_parser(self, app_name):
        parser = super(ChangeAssigneeSet, self).get_parser(app_name)
        parser.add_argument(
            '-a',
            '--account',
            required=True,
            help='The ID of one account that should be added as assignee.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.set_assignee(parsed_args.entity_id,
                                            parsed_args.account)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ChangeAssigneeDelete(BaseChangeAction):
    """Deletes the assignee of a change."""

    columns = ('_account_id',
               'name',
               'email',
               'username')

    def action(self, change_id, **kwargs):
        return self.client.delete_assignee(change_id)


class ChangeDraftPublish(ChangeMixIn, base.BaseCommand):
    """Publishes a draft change."""

    def get_parser(self, prog_name):
        parser = super(ChangeDraftPublish, self).get_parser(prog_name)
        parser.add_argument(
            'change_id',
            metavar='change-identifier',
            help='Change identifier.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.publish_draft(parsed_args.change_id)
        self.app.stdout.write("Draft change with ID {0} was successfully "
                              "published.\n".format(parsed_args.change_id))


class ChangeIncludedInSHow(BaseChangeAction):
    """Retrieves the branches and tags in which a change is included."""

    columns = ('branches',
               'tags',
               'external')

    def action(self, change_id, **kwargs):
        return self.client.get_included(change_id)


class ChangeIndex(ChangeMixIn, base.BaseCommand):
    """Adds or updates the change in the secondary index."""

    def get_parser(self, prog_name):
        parser = super(ChangeIndex, self).get_parser(prog_name)
        parser.add_argument(
            'change_id',
            metavar='change-identifier',
            help='Change identifier.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.index(parsed_args.change_id)
        msg = ("Change with ID {0} was successfully added/updated in the "
               "secondary index.\n".format(parsed_args.change_id))
        self.app.stdout.write(msg)


class ChangeCommentList(ChangeCommentMixIn, base.BaseListCommand):
    """Lists the published comments of all revisions of the change."""

    def get_parser(self, prog_name):
        parser = super(ChangeCommentList, self).get_parser(prog_name)
        parser.add_argument(
            'change_id',
            metavar='change-identifier',
            help='Change identifier.'
        )
        parser.add_argument(
            '-t',
            '--type',
            choices=['drafts', 'robotcomments'],
            default=None,
            help='The type of comments. Defaults to published.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_comments(parsed_args.change_id,
                                            comment_type=parsed_args.type)
        data = self.format_data(response)
        fetched_columns = [c for c in self.columns if data and c in data[0]]
        data = utils.get_display_data_multi(fetched_columns, data)
        return fetched_columns, data


class ChangeCheck(ChangeMixIn, base.BaseShowCommand):
    """Performs consistency checks on the change.

    Returns a ChangeInfo entity with the problems field.
    """

    def take_action(self, parsed_args):
        response = self.client.check_consistency(parsed_args.entity_id)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


class ChangeFix(ChangeMixIn, base.BaseShowCommand):
    """Performs consistency checks on the change.

    Additionally fixes any problems that can be fixed automatically. The
    returned field values reflect any fixes. Only the change owner,
    a project owner, or an administrator may fix changes.
    """

    def get_parser(self, app_name):
        parser = super(ChangeFix, self).get_parser(app_name)
        parser.add_argument(
            '--delete-patchset',
            action='store_true',
            help='Delete patch sets from the database '
                 'if they refer to missing commit options.'
        )
        parser.add_argument(
            '--expect-merged-as',
            action='store_true',
            help='Check that the change is merged into the destination branch '
                 'as this exact SHA-1. If not, insert a new patch set '
                 'referring to this commit.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.fix_consistency(
            parsed_args.entity_id,
            is_delete=parsed_args.delete_patchset,
            expect_merged_as=parsed_args.expect_merged_as)
        fetched_columns = [c for c in self.columns if c in response]
        data = utils.get_display_data_single(fetched_columns, response)
        return fetched_columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("show", ChangeShow, argv)


if __name__ == "__main__":
    debug()
