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


class ChangeMixIn(object):

    entity_name = 'change'


class ChangeShow(ChangeMixIn, base.BaseShowCommand):
    """Retrieves a change."""

    columns = ('id', 'project', 'branch', 'topic', 'hashtags', 'change_id',
               'subject', 'status', 'created', 'updated', 'submitted',
               'starred', 'stars', 'reviewed', 'submit_type', 'mergeable',
               'submittable', 'insertions', 'deletions',
               'unresolved_comment_count', '_number', 'owner', 'actions',
               'labels', 'permitted_labels', 'removable_reviewers',
               'reviewers', 'reviewer_updates', 'messages', 'current_revision',
               'revisions', '_more_changes', 'problems')

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


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("show", ChangeShow, argv)


if __name__ == "__main__":
    debug()
