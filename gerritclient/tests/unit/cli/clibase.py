import shlex
from unittest import mock

from oslotest import base as oslo_base

from gerritclient import client
from gerritclient import main as main_mod


class BaseCLITest(oslo_base.BaseTestCase):
    """Base class for testing CLI."""

    def setUp(self):
        super().setUp()

        self._get_client_patcher = mock.patch.object(client, "get_client")
        self.m_get_client = self._get_client_patcher.start()

        self.m_client = mock.MagicMock()
        self.m_get_client.return_value = self.m_client
        self.addCleanup(self._get_client_patcher.stop)

    @staticmethod
    def exec_command(command=""):
        """Executes gerrit with the specified arguments."""

        argv = shlex.split(command)
        if "--debug" not in argv:
            argv = [*argv, "--debug"]

        return main_mod.main(argv=argv)
