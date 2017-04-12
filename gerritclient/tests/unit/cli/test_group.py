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

import mock

from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_group


class TestGroupCommand(clibase.BaseCLITest):
    """Tests for gerrit group * commands."""

    def setUp(self):
        super(TestGroupCommand, self).setUp()
        self.m_client.get_all.return_value = fake_group.get_fake_groups(10)
        get_fake_group = fake_group.get_fake_group()
        self.m_client.get_by_entity_id.return_value = get_fake_group

    def test_group_list(self):
        args = 'group list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_all.assert_called_once_with()

    def test_group_show_wo_details(self):
        group_id = '1'
        args = 'group show {group_id}'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_by_entity_id.assert_called_once_with(group_id,
                                                               detailed=False)

    def test_group_show_w_details(self):
        group_id = '1'
        args = 'group show -d {group_id}'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_by_entity_id.assert_called_once_with(group_id,
                                                               detailed=True)
