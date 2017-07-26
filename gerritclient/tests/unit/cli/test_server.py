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
from gerritclient.tests.utils import fake_server


class TestConfigServerCommand(clibase.BaseCLITest):
    """Tests for gerrit config server * commands."""

    def setUp(self):
        super(TestConfigServerCommand, self).setUp()
        fake_cache_info_list = fake_server.get_fake_caches_info(5)
        self.m_client.get_caches.return_value = fake_cache_info_list
        fake_cache_info = fake_server.get_fake_cache_info()
        self.m_client.get_cache.return_value = fake_cache_info

    def test_server_version_show(self):
        args = 'server version'
        self.m_client.get_version.return_value = '2.14'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_version.assert_called_once_with()

    @mock.patch('json.dump')
    def test_server_configuration_download_json(self, m_dump):
        file_format = 'json'
        directory = '/tmp'
        test_data = fake_server.get_fake_config()
        args = 'server configuration download -f {} -d {}'.format(file_format,
                                                                  directory)
        expected_path = '{directory}/configuration.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_config.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_dump.assert_called_once_with(test_data, mock.ANY, indent=4)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_config.assert_called_once_with()

    @mock.patch('yaml.safe_dump')
    def test_server_configuration_download_yaml(self, m_safe_dump):
        file_format = 'yaml'
        directory = '/tmp'
        test_data = fake_server.get_fake_config()
        args = 'server configuration download -f {} -d {}'.format(file_format,
                                                                  directory)
        expected_path = '{directory}/configuration.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_config.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_safe_dump.assert_called_once_with(test_data, mock.ANY,
                                            default_flow_style=False)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_config.assert_called_once_with()

    @mock.patch('json.dump')
    def test_capabilities_download_json(self, m_dump):
        file_format = 'json'
        directory = '/tmp'
        test_data = fake_server.get_fake_capabilities()
        args = 'server capabilities download -f {} -d {}'.format(file_format,
                                                                 directory)
        expected_path = '{directory}/capabilities.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_capabilities.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_dump.assert_called_once_with(test_data, mock.ANY, indent=4)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_capabilities.assert_called_once_with()

    @mock.patch('yaml.safe_dump')
    def test_capabilities_download_yaml(self, m_safe_dump):
        file_format = 'yaml'
        directory = '/tmp'
        test_data = fake_server.get_fake_capabilities()
        args = 'server capabilities download -f {} -d {}'.format(file_format,
                                                                 directory)
        expected_path = '{directory}/capabilities.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_capabilities.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_safe_dump.assert_called_once_with(test_data, mock.ANY,
                                            default_flow_style=False)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_capabilities.assert_called_once_with()

    def test_server_cache_list(self):
        args = 'server cache list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_caches.assert_called_once_with()

    def test_server_cache_show(self):
        fake_cache = 'fake_cache'
        args = 'server cache show {name}'.format(name=fake_cache)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_cache.assert_called_once_with(fake_cache)

    def test_server_cache_flush_all(self):
        args = 'server cache flush --all'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.flush_caches.assert_called_once_with(is_all=True,
                                                           names=None)

    def test_server_cache_flush_several(self):
        fake_caches = ['fake_cache_1', 'fake_cache_2']
        args = 'server cache flush --name {}'.format(' '.join(fake_caches))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.flush_caches.assert_called_once_with(is_all=False,
                                                           names=fake_caches)

    @mock.patch('sys.stderr')
    def test_server_cache_flush_w_mutually_exclusive_params_fail(self,
                                                                 m_stderr):
        args = 'server cache flush --name fake_cache1 fake_cache_2 --all'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('not allowed', m_stderr.write.call_args_list[-1][0][0])

    @mock.patch('sys.stderr')
    def test_server_cache_flush_wo_params_fail(self, m_stderr):
        args = 'server cache flush'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('error: one of the arguments',
                      m_stderr.write.call_args_list[-1][0][0])

    def test_server_get_summary_state_show(self):
        args = 'server state show --max-width 110'
        fake_summary_state = fake_server.get_fake_summary_state()
        self.m_client.get_summary_state.return_value = fake_summary_state
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_summary_state.assert_called_once_with(False, False)

    def test_server_get_summary_state_show_w_jvm_gc(self):
        args = 'server state show --jvm --gc --max-width 110'
        fake_summary_state = fake_server.get_fake_summary_state()
        self.m_client.get_summary_state.return_value = fake_summary_state
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_summary_state.assert_called_once_with(True, True)

    def test_server_task_list(self):
        args = 'server task list'
        fake_task_list = fake_server.get_fake_tasks(5)
        self.m_client.get_tasks.return_value = fake_task_list
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_tasks.assert_called_once_with()

    def test_server_task_show(self):
        task_id = "62dc1cee"
        args = 'server task show {task_id}'.format(task_id=task_id)
        fake_task = fake_server.get_fake_task(task_id=task_id)
        self.m_client.get_tasks.return_value = fake_task
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_task.assert_called_once_with(task_id)

    def test_server_task_delete(self):
        task_id = "62dc1cee"
        args = 'server task delete {task_id}'.format(task_id=task_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.delete_task.assert_called_once_with(task_id)
