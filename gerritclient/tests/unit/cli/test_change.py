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

import json
import mock

from gerritclient.tests.unit.cli import clibase
from gerritclient.tests.utils import fake_account
from gerritclient.tests.utils import fake_change
from gerritclient.tests.utils import fake_comment


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
            identifier=change_id)
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
            identifier=change_id)
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
            identifier=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(change_id=change_id,
                                                        detailed=False,
                                                        options=options)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_change_create(self):
        test_data = {'project': 'myProject',
                     'subject': 'Fake subject',
                     'branch': 'master',
                     'topic': 'create-change-in-browser'}
        expected_path = '/tmp/fakes/fake-change.json'
        args = 'change create {0}'.format(expected_path)
        self.m_client.create.return_value = fake_change.get_fake_change(
            **test_data)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'r')
        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.create.assert_called_once_with(test_data)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_change_create_bad_file_format_fail(self):
        test_data = {}
        expected_path = '/tmp/fakes/bad_file.format'
        args = 'change create {0}'.format(expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.assertRaisesRegexp(ValueError, "Unsupported data format",
                                    self.exec_command, args)

    def test_change_delete(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change delete {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.delete.assert_called_once_with(change_id)

    def test_change_abandon(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change abandon {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.abandon.assert_called_once_with(change_id)

    def test_change_restore(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change restore {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.restore.assert_called_once_with(change_id)

    def test_change_revert(self):
        message = 'Fake message'
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change revert {change_id} --message "{message}"'.format(
            change_id=change_id, message=message)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.revert.assert_called_once_with(change_id,
                                                     message=message)

    def test_change_rebase(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change rebase {change_id} '.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.rebase.assert_called_once_with(change_id, parent=None)

    def test_change_rebase_w_parent(self):
        base = '6f0aea35251c48692e7e88ee3bc2bfa53684cd39'
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change rebase {change_id} --parent {base} '.format(
            change_id=change_id, base=base)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.rebase.assert_called_once_with(change_id, parent=base)

    def test_change_move(self):
        message = 'Fake message'
        branch = 'fake-branch'
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change move {change_id} -b {branch} -m "{message}"'.format(
            change_id=change_id, branch=branch, message=message)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.move.assert_called_once_with(change_id,
                                                   branch,
                                                   message=message)

    def test_change_submit_wo_parameters(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change submit {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.submit.assert_called_once_with(change_id,
                                                     on_behalf_of=None,
                                                     notify='ALL')

    def test_change_submit_w_parameters(self):
        notify = 'NONE'
        username = 'jdoe'
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = ('change submit {change_id} --on-behalf-of {username} '
                '--notify {notify}').format(change_id=change_id,
                                            username=username,
                                            notify=notify)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.submit.assert_called_once_with(change_id,
                                                     on_behalf_of=username,
                                                     notify=notify)

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

    def test_change_topic_delete(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change topic delete {change_id}'.format(change_id=change_id)
        self.m_client.delete_topic.return_value = {}
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.delete_topic.assert_called_once_with(change_id)

    def test_change_assignee_show(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change assignee show {change_id}'.format(change_id=change_id)
        account = fake_account.get_fake_account()
        self.m_client.get_assignee.return_value = account
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_assignee.assert_called_once_with(change_id)

    def test_change_assignee_history_show(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change assignee history show {change_id}'.format(
            change_id=change_id)
        fake_accounts = fake_account.get_fake_accounts(3)
        self.m_client.get_assignee.return_value = fake_accounts
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_assignees.assert_called_once_with(change_id)

    def test_change_assignee_set(self):
        account = {'_account_id': 26071983,
                   'name': 'John Doe',
                   'username': 'jdoe',
                   'email': 'jdoe@example.com'}
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change assignee set {change_id} --account {account}'.format(
            change_id=change_id, account=account['username'])
        account = fake_account.get_fake_account(**account)
        self.m_client.set_assignee.return_value = account
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.set_assignee.assert_called_once_with(change_id,
                                                           account['username'])

    def test_change_assignee_delete(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change assignee delete {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.delete_assignee.assert_called_once_with(change_id)

    def test_change_draft_publish(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change draft publish {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.publish_draft.assert_called_once_with(change_id)

    def test_change_included_get(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change included-in show {change_id}'.format(
            change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_included.assert_called_once_with(change_id)

    def test_change_index(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change index {change_id}'.format(change_id=change_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.index.assert_called_once_with(change_id)

    def test_change_comments_list(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change comment list {change_id} --max-width 110'.format(
            change_id=change_id)
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_comments.assert_called_once_with(change_id,
                                                           comment_type=None)

    def test_change_draft_comments_list(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = ('change comment list {change_id} --type drafts '
                '--max-width 110'.format(change_id=change_id))
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_comments.assert_called_once_with(
            change_id, comment_type='drafts')

    def test_change_robotcomments_list(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = ('change comment list {change_id} --type robotcomments '
                '--max-width 110'.format(change_id=change_id))
        fake_comments = fake_comment.get_fake_comments_in_change(3)
        self.m_client.get_comments.return_value = fake_comments
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.get_comments.assert_called_once_with(
            change_id, comment_type='robotcomments')

    @mock.patch('sys.stderr')
    def test_change_comments_list_w_wrong_type_fail(self, mocked_stderr):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change comment list {change_id} --type bad_comment'.format(
            change_id=change_id)
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn("invalid choice: 'bad_comment'",
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_change_consistency_check(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change check {change_id} --max-width 110'.format(
            change_id=change_id)
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.check_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.check_consistency.assert_called_once_with(change_id)

    def test_change_consistency_check_and_fix(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = 'change fix {change_id} --max-width 110'.format(
            change_id=change_id)
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.fix_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.fix_consistency.assert_called_once_with(
            change_id, is_delete=False, expect_merged_as=False)

    def test_change_consistency_check_and_fix_w_parameters(self):
        change_id = 'I8473b95934b5732ac55d26311a706c9c2bde9940'
        args = ('change fix {change_id} --delete-patchset --expect-merged-as '
                '--max-width 110'.format(change_id=change_id))
        change = fake_change.get_fake_change(identifier=change_id)
        self.m_client.fix_consistency.return_value = change
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('change', mock.ANY)
        self.m_client.fix_consistency.assert_called_once_with(
            change_id, is_delete=True, expect_merged_as=True)
