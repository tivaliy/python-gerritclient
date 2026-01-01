"""Pytest fixtures for gerritclient tests."""

import shlex
from unittest import mock

import pytest

from gerritclient import client
from gerritclient import main as main_mod


@pytest.fixture
def mock_client():
    """Fixture that provides a mocked gerrit client."""
    with mock.patch.object(client, "get_client") as m_get_client:
        m_client = mock.MagicMock()
        m_get_client.return_value = m_client
        yield {"get_client": m_get_client, "client": m_client}


def exec_command(command=""):
    """Executes gerrit with the specified arguments."""
    argv = shlex.split(command)
    if "--debug" not in argv:
        argv = [*argv, "--debug"]
    return main_mod.main(argv=argv)
