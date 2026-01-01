"""Base class for CLI tests using pytest."""

import shlex
from unittest import mock

import pytest

from gerritclient import client
from gerritclient import main as main_mod


class BaseCLITest:
    """Base class for testing CLI."""

    @pytest.fixture(autouse=True)
    def setup_client_mock(self):
        """Set up mocked client for each test."""
        with mock.patch.object(client, "get_client") as m_get_client:
            self.m_client = mock.MagicMock()
            m_get_client.return_value = self.m_client
            self.m_get_client = m_get_client
            yield

    @staticmethod
    def exec_command(command=""):
        """Executes gerrit with the specified arguments."""
        argv = shlex.split(command)
        if "--debug" not in argv:
            argv = [*argv, "--debug"]
        return main_mod.main(argv=argv)
