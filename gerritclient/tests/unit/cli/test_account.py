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


class TestAccountCommand(clibase.BaseCLITest):
    """Tests for gerrit account * commands."""

    def setUp(self):
        super(TestAccountCommand, self).setUp()
        self.m_client.get_all.return_value = fake_account.get_fake_accounts(10)
        self.m_client.get_by_id.return_value = fake_account.get_fake_account()

    def exec_list_command(self, cmd, **kwargs):
        query = 'fake-name'
        self.exec_command('{cmd} {query}'.format(cmd=cmd, query=query))

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            query,
            suggested=kwargs.get('suggested', False),
            limit=kwargs.get('limit'),
            skip=kwargs.get('skip'),
            detailed=kwargs.get('detailed', False),
            all_emails=kwargs.get('all_emails', False)
        )

    def test_account_list(self):
        args = 'account list'
        self.exec_list_command(args)

    def test_account_list_w_suggestions(self):
        args = 'account list --suggest'
        self.exec_list_command(args, suggested=True)

    def test_account_list_w_suggestions_limit(self):
        limit = 5
        fake_accounts = fake_account.get_fake_accounts(limit)
        self.m_client.get_all.return_value = fake_accounts
        args = 'account list --suggest --limit {limit}'.format(limit=limit)
        self.exec_list_command(args, limit=limit, suggested=True)

    def test_account_list_w_suggestions_skip(self):
        skip = 5
        args = 'account list --suggest --skip {skip}'.format(skip=skip)
        self.exec_list_command(args, skip=skip, suggested=True)

    def test_account_list_w_details(self):
        args = 'account list --all'
        self.exec_list_command(args, detailed=True)

    def test_account_list_w_details_all_emails(self):
        args = 'account list --all --all-emails'
        self.exec_list_command(args, detailed=True, all_emails=True)

    def test_account_list_w_details_all_emails_limit_skip(self):
        skip = 5
        limit = 10
        args = 'account list --all --all-emails --limit {0} --skip {1}'.format(
            limit, skip)
        self.exec_list_command(args, detailed=True, all_emails=True,
                               limit=limit, skip=skip)

    def test_account_show(self):
        account_id = 'john'
        args = 'account show {account_id}'.format(account_id=account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(account_id,
                                                        detailed=False)

    @mock.patch('sys.stderr')
    def test_account_show_fail(self, mocked_stderr):
        args = 'account show'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('account show: error:',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_account_show_w_details(self):
        account_id = 'john'
        args = 'account show {account_id} --all'.format(account_id=account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(account_id,
                                                        detailed=True)

    def test_account_create_w_default_parameters(self):
        username = 'fake-user'
        args = 'account create {0}'.format(username)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.create.assert_called_once_with(username, data=None)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_account_create_w_parameters_from_file(self):
        username = 'fake-user'
        test_data = {'username': username,
                     'name': 'Fake User',
                     'groups': ['Fake Group']}
        expected_path = '/tmp/fakes/fake-account.yaml'
        args = 'account create {0} --file {1}'.format(username,
                                                      expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'r')
        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.create.assert_called_once_with(username,
                                                     data=test_data)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_account_create_w_parameters_from_bad_file_format_fail(self):
        username = 'fake-user'
        test_data = {}
        expected_path = '/tmp/fakes/bad_file.format'
        args = 'account create {0} --file {1}'.format(username,
                                                      expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.assertRaisesRegexp(ValueError, "Unsupported data format",
                                    self.exec_command, args)

    @mock.patch('sys.stderr')
    def test_account_create_fail(self, mocked_stderr):
        args = 'account create'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('account create: error:',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_account_set_fullname(self):
        account_id = '69'
        name = 'Fake Name'
        args = 'account name set {0} "{1}"'.format(account_id, name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_name.assert_called_once_with(account_id,
                                                       name=name)

    def test_account_set_username(self):
        account_id = '69'
        username = 'jdoe'
        args = 'account username set {0} {1}'.format(account_id, username)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_username.assert_called_once_with(account_id,
                                                           username=username)

    def test_account_enable(self):
        account_id = '69'
        args = 'account enable {0}'.format(account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.enable.assert_called_once_with(account_id)

    def test_account_disable(self):
        account_id = '69'
        args = 'account disable {0}'.format(account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.disable.assert_called_once_with(account_id)

    def test_account_set_password(self):
        account_id = '69'
        password = 'fake-password'
        args = 'account password set {0} --password {1}'.format(account_id,
                                                                password)
        self.m_client.set_password.return_value = password
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_password.assert_called_once_with(account_id,
                                                           password,
                                                           False)

    def test_account_set_empty_password(self):
        account_id = '69'
        empty_password = ''
        args = 'account password set {0} --password "{1}"'.format(
            account_id,
            empty_password)
        self.m_client.set_password.return_value = empty_password
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_password.assert_called_once_with(account_id,
                                                           empty_password,
                                                           False)

    def test_account_generate_password(self):
        account_id = '69'
        args = 'account password set {0} --generate'.format(account_id)
        password = 'khbasdl09|asd'
        self.m_client.set_password.return_value = password
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_password.assert_called_once_with(account_id,
                                                           None,
                                                           True)
