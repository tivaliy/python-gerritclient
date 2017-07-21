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

    @mock.patch('json.dump')
    def test_server_caches_info_download_json(self, m_dump):
        file_format = 'json'
        directory = '/tmp'
        test_data = fake_server.get_fake_caches_info(5)
        args = 'server cache-info download -f {} -d {}'.format(file_format,
                                                               directory)
        expected_path = '{directory}/caches.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_caches.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_dump.assert_called_once_with(test_data, mock.ANY, indent=4)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_caches.assert_called_once_with()

    @mock.patch('yaml.safe_dump')
    def test_server_caches_info_download_yaml(self, m_safe_dump):
        file_format = 'yaml'
        directory = '/tmp'
        test_data = fake_server.get_fake_caches_info(5)
        args = 'server cache-info download -f {} -d {}'.format(file_format,
                                                               directory)
        expected_path = '{directory}/caches.{file_format}'.format(
            directory=directory, file_format=file_format)

        self.m_client.get_caches.return_value = test_data

        m_open = mock.mock_open()
        with mock.patch('gerritclient.commands.server.open',
                        m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'w')
        m_safe_dump.assert_called_once_with(test_data, mock.ANY,
                                            default_flow_style=False)
        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_caches.assert_called_once_with()

    def test_server_cache_list_text(self):
        fake_caches = ['fake-cache1', 'fake-cache2', 'fake-cache3']
        args = 'server cache list --format text'
        self.exec_command(args)

        self.m_client.get_caches.return_value = '\n'.join(fake_caches)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_caches.assert_called_once_with(
            formatting='text_list')

    def test_server_cache_list_json(self):
        fake_caches = [u'fake-cache1', u'fake-cache2', u'fake-cache3']
        args = 'server cache list --format json'
        self.exec_command(args)

        self.m_client.get_caches.return_value = fake_caches

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_caches.assert_called_once_with(
            formatting='list')

    @mock.patch('sys.stderr')
    def test_server_cache_list_bad_format_fail(self, mocked_stderr):
        args = 'server cache list --format bad_format'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('error: argument -f/--format',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_server_cache_show(self):
        fake_cache = 'fake_cache'
        args = 'server cache show {name}'.format(name=fake_cache)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('server', mock.ANY)
        self.m_client.get_cache.assert_called_once_with(fake_cache)
