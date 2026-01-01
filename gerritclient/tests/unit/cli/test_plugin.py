import os
from unittest import mock

import pytest

from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_plugin


class TestPluginCommand(clibase.BaseCLITest):
    """Tests for gerrit plugin * commands."""

    @pytest.fixture(autouse=True)
    def setup_plugin_mocks(self, setup_client_mock):
        """Set up plugin-specific mocks."""
        self.m_client.get_all.return_value = fake_plugin.get_fake_plugins(10)
        get_fake_plugin = fake_plugin.get_fake_plugin(plugin_id="fake-plugin")
        self.m_client.get_by_id.return_value = get_fake_plugin

    def test_plugin_list_enabled(self):
        args = "plugin list"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=False)

    def test_plugin_list_all(self):
        args = "plugin list --all"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.get_all.assert_called_once_with(detailed=True)

    def test_plugin_show(self):
        plugin_id = "fake-plugin"
        args = f"plugin show {plugin_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(plugin_id)

    def test_plugin_enable(self):
        plugin_id = "fake-plugin"
        args = f"plugin enable {plugin_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.enable.assert_called_once_with(plugin_id)

    def test_plugin_disable(self):
        plugin_id = "fake-plugin"
        args = f"plugin disable {plugin_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.disable.assert_called_once_with(plugin_id)

    @mock.patch("sys.stderr")
    def test_plugin_enable_fail(self, mocked_stderr):
        args = "plugin enable"
        with pytest.raises(SystemExit):
            self.exec_command(args)
        assert "plugin enable: error:" in mocked_stderr.write.call_args_list[-1][0][0]

    @mock.patch("sys.stderr")
    def test_plugin_disable_fail(self, mocked_stderr):
        args = "plugin disable"
        with pytest.raises(SystemExit):
            self.exec_command(args)
        assert "plugin disable: error:" in mocked_stderr.write.call_args_list[-1][0][0]

    def test_plugin_reload(self):
        plugin_id = "fake-plugin"
        args = f"plugin reload {plugin_id}"
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.reload.assert_called_once_with(plugin_id)

    def test_plugin_install_from_url(self):
        plugin_id = "fake-plugin.jar"
        url = "http://url/path/to/plugin.jar"
        args = f"plugin install {plugin_id} --url {url}"
        self.m_client.install.return_value = fake_plugin.get_fake_plugin(plugin_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.install.assert_called_once_with(
            plugin_id, source_type="url", value=url
        )

    @mock.patch("gerritclient.common.utils.file_exists", mock.Mock(return_value=True))
    def test_plugin_install_from_file(self):
        plugin_id = "fake-plugin.jar"
        expected_path = "/tmp/fakes/fake-plugin.jar"
        data = os.urandom(12)
        self.m_client.install.return_value = fake_plugin.get_fake_plugin(plugin_id)
        args = f"plugin install {plugin_id} --file {expected_path}"

        m_open = mock.mock_open(read_data=data)
        with mock.patch("gerritclient.commands.plugin.open", m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, "rb")
        self.m_get_client.assert_called_once_with("plugin", mock.ANY)
        self.m_client.install.assert_called_once_with(
            plugin_id, source_type="file", value=data
        )

    @mock.patch("sys.stderr")
    def test_plugin_install_w_wrong_identifier_fail(self, mocked_stderr):
        plugin_id = "bad-plugin-identifier"
        url = "http://url/path/to/plugin.jar"
        args = f"plugin install {plugin_id} --url {url}"
        result = self.exec_command(args)
        assert result == 1
        stderr_output = "".join(
            call[0][0] for call in mocked_stderr.write.call_args_list
        )
        assert 'Plugin identifier must contain ".jar"' in stderr_output
