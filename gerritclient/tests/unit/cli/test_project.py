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
from gerritclient.tests.utils import fake_project


class TestProjectCommand(clibase.BaseCLITest):
    """Tests for gerrit project * commands."""

    def setUp(self):
        super(TestProjectCommand, self).setUp()
        self.m_client.get_all.return_value = fake_project.get_fake_projects(10)
        get_fake_project = fake_project.get_fake_project()
        self.m_client.get_by_entity_id.return_value = get_fake_project

    def test_project_list_all_wo_description_wo_branches(self):
        args = 'project list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_wo_weblinkinfo_in_project_entity(self):
        fake_projects = fake_project.get_fake_projects(5, is_weblinkinfo=False)
        self.m_client.get_all.return_value = fake_projects
        args = 'project list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_all_w_description_wo_branches(self):
        args = 'project list --description'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=True,
                                                      branches=None)

    def test_project_list_all_wo_description_w_branches(self):
        branches = ['master', 'fake_branch']
        args = 'project list --branches {0}'.format(' '.join(branches))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=branches)

    def test_project_list_limit(self):
        list_limit = '5'
        args = 'project list --limit {0}'.format(list_limit)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=list_limit,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_skip_first(self):
        list_skip = '5'
        args = 'project list --skip {0}'.format(list_skip)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=list_skip,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_range(self):
        list_skip = '2'
        list_limit = '2'
        args = 'project list --skip {0} --limit {1}'.format(list_skip,
                                                            list_limit)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=list_limit,
                                                      s=list_skip,
                                                      prefix=None,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_w_prefix(self):
        prefix = 'fake'
        args = 'project list --prefix {0}'.format(prefix)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=prefix,
                                                      match=None,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_w_match(self):
        substring = 'project'
        args = 'project list --match {0}'.format(substring)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=substring,
                                                      regex=None,
                                                      description=False,
                                                      branches=None)

    @mock.patch('sys.stderr')
    def test_project_list_with_mutually_exclusive_params(self, mocked_stderr):
        args = 'project list --match some --prefix fake --regex fake*.*'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('not allowed',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_project_list_w_regex(self):
        regex = 'fake*.*'
        args = 'project list --regex {0}'.format(regex)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(n=None,
                                                      s=None,
                                                      prefix=None,
                                                      match=None,
                                                      regex=regex,
                                                      description=False,
                                                      branches=None)

    def test_project_show(self):
        project_id = 'fakes%2Ffake-project'
        args = 'project show {project_id}'.format(project_id=project_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_by_entity_id.assert_called_once_with(project_id)
