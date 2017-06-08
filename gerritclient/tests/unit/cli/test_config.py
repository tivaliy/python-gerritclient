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


class TestConfigServerCommand(clibase.BaseCLITest):
    """Tests for gerrit config server * commands."""

    def setUp(self):
        super(TestConfigServerCommand, self).setUp()

    def test_server_version_show(self):
        args = 'server version'
        self.m_client.get_version.return_value = '2.14'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('config', mock.ANY)
        self.m_client.get_version.assert_called_once_with()
