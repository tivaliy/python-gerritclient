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
                      'capabilities': self.client.get_capabilities}
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


class ServerCacheList(ServerMixIn, base.BaseListCommand):
    """Show the cache names as a list."""

    columns = ('name',
               'type',
               'entries',
               'average_get',
               'hit_ratio')

    def take_action(self, parsed_args):
        response = self.client.get_caches()
        data = self._reformat_data(response)
        data = utils.get_display_data_multi(self.columns, data)
        return self.columns, data


class ServerCacheShow(ServerMixIn, base.BaseCommand, base.show.ShowOne):
    """Retrieves information about a cache."""

    columns = ('name',
               'type',
               'entries',
               'average_get',
               'hit_ratio')

    def get_parser(self, app_name):
        parser = super(ServerCacheShow, self).get_parser(app_name)
        parser.add_argument(
            'name',
            help='Cache name.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_cache(parsed_args.name)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ServerCacheFlush(ServerMixIn, base.BaseCommand):
    """Flushes a cache."""

    def get_parser(self, prog_name):
        parser = super(ServerCacheFlush, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-a',
            '--all',
            action='store_true',
            help='All available caches.'
        )
        group.add_argument(
            '-n',
            '--name',
            nargs='+',
            help='Caches names.'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.flush_caches(is_all=parsed_args.all,
                                 names=parsed_args.name)
        msg = "The following caches were flushed: {}\n".format(
            'ALL' if parsed_args.all else ', '.join(parsed_args.name))
        self.app.stdout.write(msg)


class ServerStateSummaryList(ServerMixIn, base.BaseCommand, base.show.ShowOne):
    """Retrieves a summary of the current server state."""

    columns = ('task_summary',
               'mem_summary',
               'thread_summary')

    def get_parser(self, prog_name):
        parser = super(ServerStateSummaryList, self).get_parser(prog_name)
        parser.add_argument(
            '--jvm',
            action='store_true',
            help='Includes a JVM summary.'
        )
        parser.add_argument(
            '--gc',
            action='store_true',
            help='Requests a Java garbage collection before computing '
                 'the information about the Java memory heap.'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_summary_state(parsed_args.jvm,
                                                 parsed_args.gc)
        if parsed_args.jvm:
            self.columns += ('jvm_summary',)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ServerTaskList(ServerMixIn, base.BaseListCommand):
    """Lists the tasks from the background work queues that the Gerrit daemons

    is currently performing, or will perform in the near future.
    """

    columns = ('id',
               'state',
               'start_time',
               'delay',
               'command',
               'remote_name',
               'project')

    def take_action(self, parsed_args):
        response = self.client.get_tasks()
        data = utils.get_display_data_multi(self.columns, response)
        return self.columns, data


class ServerTaskShow(ServerMixIn, base.BaseCommand, base.show.ShowOne):
    """Retrieves a task from the background work queue that the Gerrit daemon

    is currently performing, or will perform in the near future.
    """

    columns = ('id',
               'state',
               'start_time',
               'delay',
               'command',
               'remote_name',
               'project')

    def get_parser(self, prog_name):
        parser = super(ServerTaskShow, self).get_parser(prog_name)
        parser.add_argument(
            'task_id',
            metavar='task-identifier',
            help='The ID of the task (hex string).'
        )
        return parser

    def take_action(self, parsed_args):
        response = self.client.get_task(parsed_args.task_id)
        data = utils.get_display_data_single(self.columns, response)
        return self.columns, data


class ServerTaskDelete(ServerMixIn, base.BaseCommand):
    """Kills a task from the background work queue that the Gerrit daemon

    is currently performing, or will perform in the near future.
    """

    def get_parser(self, prog_name):
        parser = super(ServerTaskDelete, self).get_parser(prog_name)
        parser.add_argument(
            'task_id',
            metavar='task-identifier',
            help='The ID of the task (hex string).'
        )
        return parser

    def take_action(self, parsed_args):
        self.client.delete_task(parsed_args.task_id)
        msg = "Task with ID '{0}' was deleted\n".format(parsed_args.task_id)
        self.app.stdout.write(msg)


def debug(argv=None):
    """Helper to debug the required command."""

    from gerritclient.main import debug
    debug("version", ServerVersionShow, argv)


if __name__ == "__main__":
    debug()
