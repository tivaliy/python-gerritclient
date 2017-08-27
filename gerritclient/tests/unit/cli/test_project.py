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
from gerritclient.tests.utils import fake_project


class TestProjectCommand(clibase.BaseCLITest):
    """Tests for gerrit project * commands."""

    def setUp(self):
        super(TestProjectCommand, self).setUp()
        self.m_client.get_all.return_value = fake_project.get_fake_projects(10)
        get_fake_project = fake_project.get_fake_project()
        self.m_client.get_by_name.return_value = get_fake_project

    def test_project_list_all_wo_description_wo_branches(self):
        args = 'project list --all'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=True,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_wo_weblinkinfo_in_project_entity(self):
        fake_projects = fake_project.get_fake_projects(5, is_weblinkinfo=False)
        self.m_client.get_all.return_value = fake_projects
        args = 'project list'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_all_w_description_wo_branches(self):
        args = 'project list --description --all'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=True,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=True,
                                                      branches=None)

    def test_project_list_all_wo_description_w_branches(self):
        branches = ['master', 'fake_branch']
        args = 'project list --all --branches {0}'.format(' '.join(branches))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=True,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=branches)

    def test_project_list_limit(self):
        list_limit = 5
        args = 'project list --limit {0}'.format(list_limit)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=list_limit,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_skip_first(self):
        list_skip = 5
        args = 'project list --skip {0}'.format(list_skip)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=None,
                                                      skip=list_skip,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_range(self):
        list_skip = 2
        list_limit = 2
        args = 'project list --skip {0} --limit {1}'.format(list_skip,
                                                            list_limit)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=list_limit,
                                                      skip=list_skip,
                                                      pattern_dispatcher=None,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_w_prefix(self):
        prefix = {'prefix': 'fake'}
        args = 'project list --prefix {0}'.format(prefix['prefix'])
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            is_all=False,
            limit=None,
            skip=None,
            pattern_dispatcher=prefix,
            project_type=None,
            description=False,
            branches=None)

    def test_project_list_w_match(self):
        match = {'match': 'project'}
        args = 'project list --match {0}'.format(match['match'])
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(
            is_all=False,
            limit=None,
            skip=None,
            pattern_dispatcher=match,
            project_type=None,
            description=False,
            branches=None)

    @mock.patch('sys.stderr')
    def test_project_list_with_mutually_exclusive_params(self, mocked_stderr):
        args = 'project list --match some --prefix fake --regex fake*.*'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('not allowed',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_project_list_w_regex(self):
        regex = {'regex': 'fake*.*'}
        args = 'project list --regex {0}'.format(regex['regex'])
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=regex,
                                                      project_type=None,
                                                      description=False,
                                                      branches=None)

    def test_project_list_w_specified_type(self):
        prj_type = 'code'
        args = 'project list --type {0}'.format(prj_type)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_all.assert_called_once_with(is_all=False,
                                                      limit=None,
                                                      skip=None,
                                                      pattern_dispatcher=None,
                                                      project_type=prj_type,
                                                      description=False,
                                                      branches=None)

    def test_project_show(self):
        project_id = 'fakes/fake-project'
        args = 'project show {project_id}'.format(project_id=project_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_by_name.assert_called_once_with(project_id)

    def test_project_create_w_default_parameters(self):
        project_id = 'fake-project'
        args = 'project create {0}'.format(project_id)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.create.assert_called_once_with(project_id, data=None)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_project_create_w_parameters_from_file(self):
        project_id = 'fakes/fake-project'
        test_data = {'name': project_id,
                     'description': 'Fake project description',
                     'owners': ['Fake Owner']}
        expected_path = '/tmp/fakes/fake-project.yaml'
        args = 'project create {0} --file {1}'.format(project_id,
                                                      expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.exec_command(args)

        m_open.assert_called_once_with(expected_path, 'r')
        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.create.assert_called_once_with(project_id,
                                                     data=test_data)

    @mock.patch('gerritclient.common.utils.file_exists',
                mock.Mock(return_value=True))
    def test_project_create_w_parameters_from_bad_file_format_fail(self):
        project_id = 'fakes/fake-project'
        test_data = {}
        expected_path = '/tmp/fakes/bad_file.format'
        args = 'project create {0} --file {1}'.format(project_id,
                                                      expected_path)

        m_open = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('gerritclient.common.utils.open', m_open, create=True):
            self.assertRaisesRegexp(ValueError, "Unsupported data format",
                                    self.exec_command, args)

    @mock.patch('sys.stderr')
    def test_project_create_fail(self, mocked_stderr):
        args = 'project create'
        self.assertRaises(SystemExit, self.exec_command, args)
        self.assertIn('project create: error:',
                      mocked_stderr.write.call_args_list[-1][0][0])

    def test_project_delete(self):
        project_name = 'fake/fake-project'
        args = 'project delete {0}'.format(project_name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.delete.assert_called_once_with(project_name,
                                                     force=False,
                                                     preserve=False)

    def test_project_delete_w_force(self):
        project_name = 'fake/fake-project'
        args = 'project delete {0} --force'.format(project_name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.delete.assert_called_once_with(project_name,
                                                     force=True,
                                                     preserve=False)

    def test_project_delete_w_preserve_git_repository(self):
        project_name = 'fake/fake-project'
        args = 'project delete {0} --preserve-git-repository'.format(
            project_name)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.delete.assert_called_once_with(project_name,
                                                     force=False,
                                                     preserve=True)

    def test_project_description_show(self):
        project_name = 'fake/fake-project'
        args = 'project description show {0}'.format(project_name)
        self.m_client.get_description.return_value = 'Fake description'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_description.assert_called_once_with(project_name)

    def test_project_description_set(self):
        project_name = 'fake/fake-project'
        project_description = 'Fake description'
        message = 'Fake commit message'
        args = ('project description set {0} --description "{1}" --message '
                '"{2}"'.format(project_name, project_description, message))
        self.m_client.set_description.return_value = project_description
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.set_description.assert_called_once_with(
            project_name,
            description=project_description,
            commit_message=message
        )

    def test_project_parent_show(self):
        project_name = 'fake/fake-project'
        args = 'project parent show {0}'.format(project_name)
        self.m_client.get_parent.return_value = 'All-Projects'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_parent.assert_called_once_with(project_name)

    def test_project_parent_set(self):
        project_name = 'fake/fake-project'
        parent_project = 'parent/fake-project'
        message = 'Fake commit message'
        args = 'project parent set {0} --parent "{1}" --message "{2}"'.format(
            project_name, parent_project, message)
        self.m_client.set_parent.return_value = parent_project
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.set_parent.assert_called_once_with(
            project_name, parent=parent_project, commit_message=message)

    def test_project_head_show(self):
        project_name = 'fake/fake-project'
        args = 'project head show {0}'.format(project_name)
        self.m_client.get_head.return_value = 'refs/heads/master'
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_head.assert_called_once_with(project_name)

    def test_project_head_set(self):
        project_name = 'fake/fake-project'
        branch = 'fake-branch'
        args = 'project head set {0} --branch {1}'.format(project_name, branch)
        self.m_client.set_head.return_value = 'refs/heads/{0}'.format(branch)
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.set_head.assert_called_once_with(project_name,
                                                       branch=branch)

    def test_project_repo_statistics_show(self):
        project_name = 'fake/fake-project'
        args = 'project repo-statistics show {0}'.format(project_name)
        fake_statistics = fake_project.get_fake_repo_statistics()
        self.m_client.get_repo_statistics.return_value = fake_statistics
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_repo_statistics.assert_called_once_with(project_name)

    def test_project_branch_list(self):
        project_name = 'fake/fake-project'
        args = 'project branch list {0}'.format(project_name)
        fake_branches = fake_project.get_fake_project_branches(5)
        self.m_client.get_branches.return_value = fake_branches
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_branches.assert_called_once_with(project_name)

    def test_project_branch_show(self):
        project_name = 'fake/fake-project'
        branch_name = 'refs/heads/fake-branch'
        args = 'project branch show {0} --branch {1}'.format(project_name,
                                                             branch_name)
        fake_branch = fake_project.get_fake_project_branch(ref=branch_name)
        self.m_client.get_branch.return_value = fake_branch
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.get_branch.assert_called_once_with(
            project_name, branch_name=branch_name)

    def test_project_branch_create(self):
        project_name = 'fake/fake-project'
        branch_name = 'refs/heads/fake-branch'
        revision = '67ebf73496383c6777035e374d2d664009e2aa5c'
        args = 'project branch create {0} --branch {1} --revision {2}'.format(
            project_name, branch_name, revision)
        fake_branch = fake_project.get_fake_project_branch(ref=branch_name,
                                                           revision=revision)
        self.m_client.create_branch.return_value = fake_branch
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.create_branch.assert_called_once_with(
            project_name, branch_name=branch_name, revision=revision)

    def test_project_branch_delete(self):
        project_name = 'fake/fake-project'
        branches = ['refs/heads/fake-branch', 'refs/heads/fake-new-branch']
        args = 'project branch delete {0} --branch {1}'.format(
            project_name, ' '.join(branches))
        self.exec_command(args)

        self.m_get_client.assert_called_once_with('project', mock.ANY)
        self.m_client.delete_branch.assert_called_once_with(
            project_name, branches)
