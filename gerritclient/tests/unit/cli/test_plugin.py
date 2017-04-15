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
from gerritclient.tests.utils import fake_plugin


class TestPluginCommand(clibase.BaseCLITest):
    """Tests for gerrit plugin * commands."""

    def setUp(self):
        super(TestPluginCommand, self).setUp()
        self.m_client.get_all.return_value = fake_plugin.get_fake_plugins(10)
        get_fake_plugin = fake_plugin.get_fake_plugin(plugin_id="fake-plugin")
        self.m_client.get_by_entity_id.return_value = get_fake_plugin

    def test_plugin_list_enabled(self):
        args = 'plugin list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=False)

    def test_plugin_list_all(self):
        args = 'plugin list --all'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=True)

    def test_plugin_show(self):
        plugin_id = 'fake-plugin'
        args = 'plugin show {plugin_id}'.format(plugin_id=plugin_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('plugin', mock.ANY)
        self.m_client.get_by_entity_id.assert_called_once_with(plugin_id)
