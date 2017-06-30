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
from gerritclient.tests.utils import fake_group


class TestGroupCommand(clibase.BaseCLITest):
    """Tests for gerrit group * commands."""

    def setUp(self):
        super(TestGroupCommand, self).setUp()
        self.m_client.get_all.return_value = fake_group.get_fake_groups(10)
        get_fake_group = fake_group.get_fake_group()
        self.m_client.get_by_id.return_value = get_fake_group
        get_fake_accounts = fake_account.get_fake_accounts(10)
        self.m_client.get_members.return_value = get_fake_accounts

    def test_group_list(self):
        args = 'group list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_all.assert_called_once_with()

    def test_group_show_wo_details(self):
        group_id = '1'
        args = 'group show {group_id}'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(group_id,
                                                        detailed=False)

    def test_group_show_w_details(self):
        group_id = '1'
        args = 'group show {group_id} --all'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_by_id.assert_called_once_with(group_id,
                                                        detailed=True)

    def test_group_member_list_wo_included_groups(self):
        group_id = '1'
        args = 'group member list {group_id}'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_members.assert_called_once_with(group_id,
                                                          detailed=False)

    def test_group_member_list_w_included_groups(self):
        group_id = '1'
        args = 'group member list {group_id} --all'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.get_members.assert_called_once_with(group_id,
                                                          detailed=True)

    def test_group_create_w_default_parameters(self):
        group_name = 'Fake-Group'
        args = 'group create {0}'.format(group_name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.create.assert_called_once_with(group_name, data=None)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_group_create_w_parameters_from_file(self):
        group_name = 'Fake-Group'
        test_data = {'name': group_name,
                     'description': 'Fake Group description',
                     'owner_id': 'Administrators',
                     'owners': 'admin'}
        expected_path = '/tmp/fakes/fake-group.yaml'
        args = 'group create {0} --file {1}'.format(group_name,
                                                    expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'r')
        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.create.assert_called_once_with(group_name,
                                                     data=test_data)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_group_create_w_parameters_from_bad_file_format_fail(self):
        group_name = 'Fake-Group'
        test_data = {}
        expected_path = '/tmp/fakes/bad_file.format'
        args = 'group create {0} --file {1}'.format(group_name,
                                                    expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.assertRaisesRegexp(ValueError, "Unsupported data format",
                                    self.exec_command, args)

    @mock.patch('sys.stderr')
    def test_group_project_fail(self, mocked_stderr):
        args = 'group create'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('group create: error:',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_group_rename(self):
        group_id = '69'
        new_name = 'New-Fake-Group'
        args = 'group rename {group_id} {new_name}'.format(group_id=group_id,
                                                           new_name=new_name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.rename.assert_called_once_with(group_id, new_name)

    def test_group_set_description(self):
        group_id = '69'
        description = 'New Fake group description'
        args = 'group description set {0} "{1}"'.format(group_id, description)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.set_description.assert_called_once_with(group_id,
                                                              description)

    def test_group_delete_description(self):
        group_id = '69'
        args = 'group description delete {group_id}'.format(group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.delete_description.assert_called_once_with(group_id)

    def test_group_set_options(self):
        group_id = '69'
        args = 'group options set {group_id} --visible'.format(
            group_id=group_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.set_options.assert_called_once_with(group_id, True)

    @mock.patch('sys.stderr')
    def test_group_set_options_fail(self, mocked_stderr):
        group_id = '69'
        args = 'group options set {group_id} --visible --no-visible'.format(
            group_id=group_id)
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('not allowed with argument',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_group_set_owner_group(self):
        group_id = '69'
        owner_group = 'Administrators'
        args = 'group owner set {group_id} {owner_group}'.format(
            group_id=group_id, owner_group=owner_group)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.set_owner_group.assert_called_once_with(group_id,
                                                              owner_group)

    def test_group_members_add(self):
        group_id = '69'
        accounts_ids = ['1013', '1014', '1015']
        args = 'group member add {group_id} --account {account_id}'.format(
            group_id=group_id, account_id=' '.join(accounts_ids))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.add_members.assert_called_once_with(group_id,
                                                          accounts_ids)

    def test_group_members_delete(self):
        group_id = '69'
        accounts_ids = ['1013', '1014', '1015']
        args = 'group member delete {group_id} --account {account_id}'.format(
            group_id=group_id, account_id=' '.join(accounts_ids))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.delete_members.assert_called_once_with(group_id,
                                                             accounts_ids)

    def test_group_include_groups(self):
        group_id = '69'
        groups_ids = ['1013', '1014', '1015']
        args = 'group include {group_id} --group {groups_ids}'.format(
            group_id=group_id, groups_ids=' '.join(groups_ids))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.include.assert_called_once_with(group_id, groups_ids)

    def test_group_exclude_groups(self):
        group_id = '69'
        groups_ids = ['1013', '1014', '1015']
        args = 'group exclude {group_id} --group {groups_ids}'.format(
            group_id=group_id, groups_ids=' '.join(groups_ids))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('group', mock.ANY)
        self.m_client.exclude.assert_called_once_with(group_id, groups_ids)
