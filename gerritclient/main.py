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

import logging
import sys

from cliff import app
from cliff.commandmanager import CommandManager


LOG = logging.getLogger(__name__)


class GerritClient(app.App):
    """Main cliff application class.

    Initialization of the command manager and configuration of basic engines.
    """
    def run(self, argv):
        return super(GerritClient, self).run(argv)


def main(argv=sys.argv[1:]):
    gerritclient_app = GerritClient(
        description='CLI tool for managing Gerrit Code Review.',
        version='0.0.1',
        command_manager=CommandManager('gerritclient',
                                       convert_underscores=True),
        deferred_help=True
    )
    return gerritclient_app.run(argv)


def debug(name, cmd_class, argv=None):
    """Helper for debugging single command without package installation."""

    import sys

    if argv is None:
        argv = sys.argv[1:]

    argv = [name] + argv + ["-v", "-v", "--debug"]
    cmd_mgr = CommandManager("test_gerritclient", convert_underscores=True)
    cmd_mgr.add_command(name, cmd_class)
    return GerritClient(
        description="CLI tool for managing Gerrit Code Review.",
        version='0.0.1',
        command_manager=cmd_mgr
    ).run(argv)
