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

import abc
import os
import six

from gerritclient.commands import base
from gerritclient.common import utils
from gerritclient import error


class ServerMixIn(object):

    entity_name = 'server'


class ServerVersionShow(ServerMixIn, base.BaseCommand):
    """Returns the version of the Gerrit server."""

    def take_action(self, parsed_args):
        self.app.stdout.write(self.client.get_version() + '\n')


@six.add_metaclass(abc.ABCMeta)
class ServerBaseDownload(ServerMixIn, base.BaseCommand):
    """Base Download class Gerrit server configuration."""

    @abc.abstractproperty
    def attribute(self):
        """Type of attribute: ('configuration'|'capabilities'|'caches')

        :rtype: str
        """
        pass

    def get_parser(self, prog_name):
        parser = super(ServerBaseDownload, self).get_parser(prog_name)
        parser.add_argument('-f',
                            '--format',
                            default='json',
                            choices=utils.SUPPORTED_FILE_FORMATS,
                            help='Format of serialized {} '
                                 'configuration.'.format(self.attribute))
        parser.add_argument('-d',
                            '--directory',
                            required=False,
                            default=os.path.curdir,
                            help='Destination directory. Defaults to '
                                 'the current directory.')
        return parser

    def take_action(self, parsed_args):
        attributes = {'configuration': self.client.get_config,
                      'capabilities': self.client.get_capabilities,
                      'caches': self.client.get_caches}
        file_path = os.path.join(os.path.abspath(parsed_args.directory),
                                 '{}.{}'.format(self.attribute,
                                                parsed_args.format))
        response_data = attributes[self.attribute]()
        try:
            if not os.path.exists(parsed_args.directory):
                os.makedirs(parsed_args.directory)
            with open(file_path, 'w') as stream:
                utils.safe_dump(parsed_args.format, stream, response_data)
        except (OSError, IOError) as e:
            msg = ("Could not store {} data at {}. "
                   "{}".format(self.attribute, file_path, e))
            raise error.InvalidFileException(msg)
        msg = "Information about {} was stored in {}\n".format(self.attribute,
                                                               file_path)
        self.app.stdout.write(msg)


class ServerConfigDownload(ServerBaseDownload):
    """Downloads the information about the Gerrit server configuration."""

    attribute = 'configuration'


class ServerCapabilitiesDownload(ServerBaseDownload):
    """Downloads a list of the capabilities available in the system."""

    attribute = 'capabilities'


class ServerCacheInfoDownload(ServerBaseDownload):
    """Downloads a list of the caches of the server."""

    attribute = 'caches'


class ServerCacheList(ServerMixIn, base.BaseCommand):
    """Show the cache names as a list."""

    def get_parser(self, prog_name):
        parser = super(ServerCacheList, self).get_parser(prog_name)
        parser.add_argument(
            '-f',
            '--format',
            default='text',
            choices=['text', 'json'],
            help='Output formats.'
        )
        return parser

    def take_action(self, parsed_args):
        format_map = {'text': 'text_list', 'json': 'list'}
        formatting = format_map[parsed_args.format]
        return self.client.get_caches(formatting=formatting)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("version", ServerVersionShow, argv)


if __name__ == "__main__":
    debug()