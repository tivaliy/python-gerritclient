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

import os

from gerritclient.commands import base
from gerritclient.common import utils
from gerritclient import error


class ConfigMixIn(object):

    entity_name = 'config'


class ServerVersionShow(ConfigMixIn, base.BaseCommand):
    """Returns the version of the Gerrit server."""

    def take_action(self, parsed_args):
        self.app.stdout.write(self.client.get_version() + '\n')


class ServerConfigDownload(ConfigMixIn, base.BaseCommand):
    """Returns the information about the Gerrit server configuration."""

    def get_parser(self, prog_name):
        parser = super(ServerConfigDownload, self).get_parser(prog_name)
        parser.add_argument('-f',
                            '--format',
                            default='json',
                            choices=utils.SUPPORTED_FILE_FORMATS,
                            help='Format of serialized server configuration.')
        parser.add_argument('-d',
                            '--directory',
                            required=False,
                            default=os.path.curdir,
                            help='Destination directory. Defaults to '
                                 'the current directory.')
        return parser

    def take_action(self, parsed_args):
        file_path = os.path.join(os.path.abspath(parsed_args.directory),
                                 'gerrit_config.{}'.format(parsed_args.format))
        response_data = self.client.get_config()
        try:
            if not os.path.exists(parsed_args.directory):
                os.makedirs(parsed_args.directory)
            with open(file_path, 'w') as stream:
                utils.safe_dump(parsed_args.format, stream, response_data)
        except (OSError, IOError) as e:
            msg = ("Could not store configuration data at {}. "
                   "{}".format(file_path, e))
            raise error.InvalidFileException(msg)
        msg = "Server configuration data was stored in {}\n".format(file_path)
        self.app.stdout.write(msg)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("version", ServerVersionShow, argv)


if __name__ == "__main__":
    debug()
