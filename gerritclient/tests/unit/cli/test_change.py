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

import mock

from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_change


class TestChangeCommand(clibase.BaseCLITest):
    """Tests for gerrit change * commands."""

    def setUp(self):
        super(TestChangeCommand, self).setUp()

    def test_change_list_w_single_query(self):
        query = ['status:open+is:watched']
        args = 'change list {query} --max-width 110'.format(
            query=''.join(query))
        self.m_client.get_all.return_value = fake_change.get_fake_changes(5)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_all.assert_called_once_with(query=query,
                                                      options=None,
                                                      limit=None,
                                                      skip=None)

    def test_change_list_w_multiple_queries(self):
        query = ['status:open+is:watched', 'is:closed+owner:self+limit:5']
        args = 'change list {query} --max-width 110'.format(
            query=' '.join(query))
        self.m_client.get_all.return_value = [fake_change.get_fake_changes(3),
                                              fake_change.get_fake_changes(2)]
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_all.assert_called_once_with(query=query,
                                                      options=None,
                                                      limit=None,
                                                      skip=None)

    def test_change_list_w_skip(self):
        skip = 2
        query = ['status:open+is:watched']
        args = 'change list {query} --skip {skip} --max-width 110'.format(
            query=''.join(query), skip=skip)
        self.m_client.get_all.return_value = fake_change.get_fake_changes(5)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_all.assert_called_once_with(query=query,
                                                      options=None,
                                                      limit=None,
                                                      skip=skip)

    def test_change_list_w_limit(self):
        limit = 2
        query = ['status:open+is:watched']
        args = 'change list {query} --limit {limit} --max-width 110'.format(
            query=''.join(query), limit=limit)
        self.m_client.get_all.return_value = fake_change.get_fake_changes(2)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_all.assert_called_once_with(query=query,
                                                      options=None,
                                                      limit=limit,
                                                      skip=None)

    def test_change_list_w_options(self):
        options = ['LABELS', 'MESSAGES', 'REVIEWED']
        query = ['status:open+is:watched']
        args = 'change list {query} --option {option} --max-width 110'.format(
            query=''.join(query), option=' '.join(options))
        self.m_client.get_all.return_value = fake_change.get_fake_changes(2)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_all.assert_called_once_with(query=query,
                                                      options=options,
                                                      limit=None,
                                                      skip=None)

    def test_change_show_wo_details(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change show {change_id} --max-width 110'.format(
            change_id=change_id)
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id=change_id,
                                                        detailed=False,
                                                        options=None)

    def test_change_show_w_details(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change show {change_id} --all --max-width 110'.format(
            change_id=change_id)
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id=change_id,
                                                        detailed=True,
                                                        options=None)

    def test_change_show_w_options(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        options = ['LABELS', 'MESSAGES', 'REVIEWED']
        args = ('change show {change_id} --option {options} '
                '--max-width 110'.format(change_id=change_id,
                                         options=' '.join(options)))
        self.m_client.get_by_id.return_value = fake_change.get_fake_change(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id=change_id,
                                                        detailed=False,
                                                        options=options)

    def test_change_topic_show(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change topic show {change_id}'.format(change_id=change_id)
        self.m_client.get_topic.return_value = 'Fake topic'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_topic.assert_called_once_with(change_id)

    def test_change_topic_set(self):
        topic = 'New fake topic'
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change topic set {change_id} --topic "{topic}"'.format(
            change_id=change_id, topic=topic)
        self.m_client.set_topic.return_value = topic
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.set_topic.assert_called_once_with(change_id,
                                                        topic)
