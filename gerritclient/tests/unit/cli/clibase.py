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

import shlex

import mock
from oslotest import base as oslo_base

from gerritclient import client
from gerritclient import main as main_mod


class BaseCLITest(oslo_base.BaseTestCase):
    """Base class for testing CLI."""

    def setUp(self):
        super(BaseCLITest, self).setUp()

        self._get_client_patcher = mock.patch.object(client,
                                                     'get_client')
        self.m_get_client = self._get_client_patcher.start()

        self.m_client = mock.MagicMock()
        self.m_get_client.return_value = self.m_client
        self.addCleanup(self._get_client_patcher.stop)

    @staticmethod
    def exec_command(command=''):
        """Executes gerrit with the specified arguments."""

        argv = shlex.split(command)
        if '--debug' not in argv:
            argv = argv + ['--debug']

        return main_mod.main(argv=argv)
