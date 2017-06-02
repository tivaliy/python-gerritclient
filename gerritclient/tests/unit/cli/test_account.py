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
from gerritclient.tests.utils import fake_sshkeyinfo


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

    def test_account_status_show(self):
        account_id = '69'
        args = 'account status show {0}'.format(account_id)
        self.m_client.is_active.return_value = True
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.is_active.assert_called_once_with(account_id)

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

    def test_account_delete_password(self):
        account_id = '69'
        args = 'account password delete {0}'.format(account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.delete_password.assert_called_once_with(account_id)

    def test_account_ssh_keys_list(self):
        account_id = '69'
        args = 'account ssh-key list {0}'.format(account_id)
        fake_ssh_keys_info = fake_sshkeyinfo.get_fake_ssh_keys_info(5)
        self.m_client.get_ssh_keys.return_value = fake_ssh_keys_info
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_ssh_keys.assert_called_once_with(account_id)

    def test_account_ssh_key_show(self):
        account_id = '69'
        sequence_id = 71
        args = 'account ssh-key show {0} --sequence-id {1}'.format(account_id,
                                                                   sequence_id)
        fake_ssh_key_info = fake_sshkeyinfo.get_fake_ssh_key_info(sequence_id)
        self.m_client.get_ssh_key.return_value = fake_ssh_key_info
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_ssh_key.assert_called_once_with(account_id,
                                                          sequence_id)

    @mock.patch('sys.stderr')
    def test_account_ssh_key_show_fail(self, mocked_stderr):
        account_id = '69'
        args = 'account ssh-key show {0}'.format(account_id)
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('ssh-key show: error:',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_account_ssh_key_add(self):
        account_id = '69'
        ssh_key = ('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0T...'
                   'YImydZAw\u003d\u003d john.doe@example.com')
        args = 'account ssh-key add {0} --ssh-key "{1}"'.format(account_id,
                                                                ssh_key)
        fake_ssh_key_info = fake_sshkeyinfo.get_fake_ssh_key_info(1)
        self.m_client.add_ssh_key.return_value = fake_ssh_key_info
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.add_ssh_key.assert_called_once_with(account_id,
                                                          ssh_key)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_account_ssh_key_add_from_file(self):
        account_id = '69'
        test_data = ('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0T...'
                     'YImydZAw\u003d\u003d john.doe@example.com')
        expected_path = '/tmp/fakes/fake-ssh-key.pub'
        args = 'account ssh-key add {0} --file {1}'.format(account_id,
                                                           expected_path)
        fake_ssh_key_info = fake_sshkeyinfo.get_fake_ssh_key_info(1)
        self.m_client.add_ssh_key.return_value = fake_ssh_key_info
        m_open = mock.mock_open(read_data=test_data)
        with mock.patch('gerritclient.commands.account.open', m_open,
                        create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'r')
        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.add_ssh_key.assert_called_once_with(account_id,
                                                          test_data)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    @mock.patch('sys.stderr')
    def test_account_ssh_key_add_fail_with_mutually_exclusive_params(
            self, mocked_stderr):
        account_id = '69'
        expected_path = '/tmp/fakes/fake-ssh-key.pub'
        ssh_key = ('ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA0T...'
                   'YImydZAw\u003d\u003d john.doe@example.com')
        args = 'account ssh-key add {0} --ssh-key "{1}" --file {2} '.format(
            account_id, ssh_key, expected_path
        )
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('not allowed',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_account_ssh_key_delete(self):
        account_id = '69'
        sequence_id = 71
        args = 'account ssh-key delete {0} --sequence-id {1}'.format(
            account_id, sequence_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.delete_ssh_key.assert_called_once_with(account_id,
                                                             sequence_id)

    def test_account_membership_list(self):
        account_id = '69'
        args = 'account membership list {0}'.format(account_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.get_membership.assert_called_once_with(account_id)

    def test_account_email_add(self):
        account_id = '69'
        email = 'jdoe@example.com'
        args = 'account email add {0} --email {1}'.format(account_id, email)
        fake_account_email_info = fake_account.get_fake_account_email_info(
            email=email)
        self.m_client.add_email.return_value = fake_account_email_info
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.add_email.assert_called_once_with(account_id,
                                                        email,
                                                        no_confirmation=False,
                                                        preferred=False)

    def test_account_email_delete(self):
        account_id = '69'
        email = 'jdoe@example.com'
        args = 'account email delete {0} --email {1}'.format(account_id, email)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.delete_email.assert_called_once_with(account_id, email)

    def test_account_email_set_as_preferred(self):
        account_id = '69'
        email = 'jdoe@example.com'
        args = 'account email set-preferred {0} {1}'.format(account_id, email)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('account', mock.ANY)
        self.m_client.set_preferred_email.assert_called_once_with(account_id,
                                                                  email=email)
