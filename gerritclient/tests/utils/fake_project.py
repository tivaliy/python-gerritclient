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


def get_fake_project(project_id="fakes%2Ffake-project",
                     name="fakes/fake-project",
                     state="ACTIVE",
                     is_single_item=True):
    """Creates a fake project

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    fake_project = {
        "id": project_id,
        "parent": "Fake-Projects",
        "description": "{project_name} description".format(project_name=name),
        "state": state,
        "branches": {
            "master": "49976b089a75e315233ab251bb9c591cfa5ed86d"
        },
        "web_links": [
            {
                "name": "gitweb",
                "url": "gitweb?p\u003d{}.git;a\u003dsummary".format(project_id)
            }
        ]
    }
    # 'name' key set only for single item, otherwise 'name' key is used
    # as map key if we try to fetch several items
    if is_single_item:
        fake_project['name'] = name
        return fake_project
    return {name: fake_project}


def get_fake_projects(projects_count):
    """Creates a random fake projects map."""

    fake_groups = {}
    for item in range(1, projects_count + 1):
        fake_groups.update(
            get_fake_project(project_id="fakes%2project-{0}".format(item),
                             name="fakes/project-{0}".format(item),
                             is_single_item=False)
        )
    return fake_groups