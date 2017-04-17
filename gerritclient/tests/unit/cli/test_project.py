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
from gerritclient.tests.utils import fake_project


class TestProjectCommand(clibase.BaseCLITest):
    """Tests for gerrit project * commands."""

    def setUp(self):
        super(TestProjectCommand, self).setUp()
        self.m_client.get_all.return_value = fake_project.get_fake_projects(10)

    def test_plugin_list_all_wo_description(self):
        args = 'project list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(description=False)

    def test_plugin_list_all_w_description(self):
        args = 'project list --description'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(description=True)
