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
        return super().run(argv)


def main(argv=sys.argv[1:]):
    gerritclient_app = GerritClient(
        description="CLI tool for managing Gerrit Code Review.",
        version="0.1.1",
        command_manager=CommandManager("gerritclient", convert_underscores=True),
        deferred_help=True,
    )
    return gerritclient_app.run(argv)


def debug(name, cmd_class, argv=None):
    """Helper for debugging single command without package installation."""

    import sys

    if argv is None:
        argv = sys.argv[1:]

    argv = [name, *argv, "-v", "-v", "--debug"]
    cmd_mgr = CommandManager("test_gerritclient", convert_underscores=True)
    cmd_mgr.add_command(name, cmd_class)
    return GerritClient(
        description="CLI tool for managing Gerrit Code Review.",
        version="0.1.1",
        command_manager=cmd_mgr,
    ).run(argv)
