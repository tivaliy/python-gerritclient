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

    columns = ('id', 'project', 'branch', 'topic', 'change_id', 'subject',
               'status', 'created', 'updated', 'submitted', 'starred',
               'stars', 'submit_type', 'mergeable', 'insertions', 'deletions',
               'unresolved_comment_count', '_number', 'owner', 'actions')

    def take_action(self, parsed_args):
        response = self.client.get_by_id(parsed_args.entity_id)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("show", ChangeShow, argv)


if __name__ == "__main__":
    debug()
