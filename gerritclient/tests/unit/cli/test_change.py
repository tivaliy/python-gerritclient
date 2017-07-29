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
from gerritclient.tests.utils import fake_change


class TestChangeCommand(clibase.BaseCLITest):
    """Tests for gerrit change * commands."""

    def setUp(self):
        super(TestChangeCommand, self).setUp()

    def test_change_show_wo_details(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change show {change_id}'.format(change_id=change_id)
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id, False)

    def test_change_show_w_details(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change show {change_id} --all --max-width 110'.format(
            change_id=change_id)
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id, True)
