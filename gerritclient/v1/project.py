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

from gerritclient.v1 import base


class ProjectClient(base.BaseV1Client):

    api_path = "projects/"

    def get_all(self, limit=None, skip=None, pattern_dispatcher=None,
                project_type=None, description=False, branches=None):
        """Get list of all available projects accessible by the caller.

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
        request_path = "{api_path}{all}".format(
            api_path=self.api_path,
            all="?d" if description else "")
        return self.connection.get_request(request_path, params=params)

    def get_by_entity_id(self, entity_id):
        request_path = "{api_path}{entity_id}".format(
            api_path=self.api_path,
            entity_id=entity_id)
        return self.connection.get_request(request_path)


def get_client(connection):
    return ProjectClient(connection)
