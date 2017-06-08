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

from gerritclient.commands import base


class ConfigMixIn(object):

    entity_name = 'config'


class ServerVersionShow(ConfigMixIn, base.BaseCommand):
    """Returns the version of the Gerrit server."""

    def take_action(self, parsed_args):
        self.app.stdout.write(self.client.get_version() + '\n')


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("version", ServerVersionShow, argv)


if __name__ == "__main__":
    debug()
