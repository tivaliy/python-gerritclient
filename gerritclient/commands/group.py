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


class GroupMixIn(object):

    entity_name = 'group'


class GroupList(GroupMixIn, base.BaseListCommand):
    """Lists all groups in Gerrit Code Review."""

    columns = ('group_id',
               'name',
               'id',
               'url',
               'options',
               'description',
               'owner',
               'owner_id')

    def take_action(self, parsed_args):
        data = self.client.get_all()
        # Retrieve group name-key from data and add it as a 'name' column
        for group_item in data:
            data[group_item]['name'] = group_item
        data = utils.get_display_data_multi(self.columns, data.values())

        return self.columns, data


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("list", GroupList, argv)


if __name__ == "__main__":
    debug()
