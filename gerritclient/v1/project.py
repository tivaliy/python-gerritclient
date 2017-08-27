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

from requests import utils as requests_utils

from gerritclient.v1 import base


class ProjectClient(base.BaseV1ClientCreateEntity):

    api_path = "/projects/"

    def get_all(self, is_all=False, limit=None, skip=None,
                pattern_dispatcher=None, project_type=None,
                description=False, branches=None):
        """Get list of all available projects accessible by the caller.

        :param is_all: boolean value, if True then all projects (including
                       hidden ones) will be added to the results
        :param limit: Int value that allows to limit the number of projects
                      to be included in the output results
        :param skip: Int value that allows to skip the given
                     number of projects from the beginning of the list
        :param pattern_dispatcher: Dict of pattern type with respective
                     pattern value: {('prefix'|'match'|'regex') : value}
        :param project_type: string value for type of projects to be fetched
                            ('code'|'permissions'|'all')
        :param description: boolean value, if True then description will be
                            added to the output result
        :param branches: List of names of branches as a string to limit the
                         results to the projects having the specified branches
                         and include the sha1 of the branches in the results
        :return: A map (dict) that maps entity names to respective entries
        """

        pattern_types = {'prefix': 'p',
                         'match': 'm',
                         'regex': 'r'}

        p, v = None, None
        if pattern_dispatcher is not None and pattern_dispatcher:
            for item in pattern_types:
                if item in pattern_dispatcher:
                    p, v = pattern_types[item], pattern_dispatcher[item]
                    break
            else:
                raise ValueError("Pattern types can be either "
                                 "'prefix', 'match' or 'regex'.")

        params = {k: v for k, v in (('n', limit),
                                    ('S', skip),
                                    (p, v),
                                    ('type', project_type),
                                    ('b', branches)) if v is not None}
        params['all'] = int(is_all)
        params['d'] = int(description)
        return self.connection.get_request(self.api_path, params=params)

    def get_by_name(self, name):
        """Get detailed info about specified project."""

        request_path = "{api_path}{name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def delete(self, name, force=False, preserve=False):
        """Delete specified project."""

        data = {"force": force,
                "preserve": preserve}
        request_path = "{api_path}{name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.delete_request(request_path, data)

    def get_description(self, name):
        """Retrieves the description of a project."""

        request_path = "{api_path}{name}/description".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def set_description(self, name, description=None, commit_message=None):

        data = {'description': description,
                'commit_message': commit_message}
        request_path = "{api_path}{name}/description".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def get_parent(self, name):

        request_path = "{api_path}{name}/parent".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def set_parent(self, name, parent, commit_message=None):

        data = {'parent': parent,
                'commit_message': commit_message}
        request_path = "{api_path}{name}/parent".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def get_head(self, name):

        request_path = "{api_path}{name}/HEAD".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def set_head(self, name, branch):

        data = {'ref': branch}
        request_path = "{api_path}{name}/HEAD".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def get_repo_statistics(self, name):

        request_path = "{api_path}{name}/statistics.git".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def get_branches(self, name):

        request_path = "{api_path}{name}/branches".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.get_request(request_path)

    def get_branch(self, name, branch_name):

        request_path = "{api_path}{name}/branches/{branch_name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''),
            branch_name=requests_utils.quote(branch_name, safe=''))
        return self.connection.get_request(request_path)

    def create_branch(self, name, branch_name, revision=None):
        """Create a new branch.

        :param name: Name of the project
        :param branch_name: Name of the branch
        :param revision: The base revision of the new branch. If not set,
                         HEAD will be used as base revision.
        :return: A BranchInfo entity that describes the created branch.
        """

        data = {'revision': revision}
        request_path = "{api_path}{name}/branches/{branch_name}".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''),
            branch_name=requests_utils.quote(branch_name, safe=''))
        return self.connection.put_request(request_path, json_data=data)

    def delete_branch(self, name, branches):
        """Delete one or more branches.

        :param name: Name of the project
        :param branches: A list of branch names that identify the branches
                         that should be deleted.
        """

        data = {'branches': branches}
        request_path = "{api_path}{name}/branches:delete".format(
            api_path=self.api_path,
            name=requests_utils.quote(name, safe=''))
        return self.connection.post_request(request_path, json_data=data)


def get_client(connection):
    return ProjectClient(connection)
