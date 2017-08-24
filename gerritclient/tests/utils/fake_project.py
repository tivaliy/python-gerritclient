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

from gerritclient.tests.utils import fake_weblinkifno


def get_fake_project(project_id="fakes%2Ffake-project",
                     name="fakes/fake-project",
                     state="ACTIVE",
                     is_weblinkinfo=True,
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
    }
    if is_weblinkinfo:
        fake_project['web_links'] = fake_weblinkifno.get_fake_weblinkinfo(
            project_id=project_id
        )
    # 'name' key set only for single item, otherwise 'name' key is used
    # as map key if we try to fetch several items
    if is_single_item:
        fake_project['name'] = name
        return fake_project
    return {name: fake_project}


def get_fake_projects(projects_count, is_weblinkinfo=True):
    """Creates a random fake projects map."""

    fake_groups = {}
    for item in range(1, projects_count + 1):
        fake_groups.update(
            get_fake_project(project_id="fakes%2project-{0}".format(item),
                             name="fakes/project-{0}".format(item),
                             is_single_item=False,
                             is_weblinkinfo=is_weblinkinfo)
        )
    return fake_groups


def get_fake_repo_statistics():
    """Creates a random fake repo statistics."""

    return {
        "number_of_loose_objects": 127,
        "number_of_loose_refs": 15,
        "number_of_pack_files": 15,
        "number_of_packed_objects": 67,
        "number_of_packed_refs": 0,
        "size_of_loose_objects": 29466,
        "size_of_packed_objects": 9646
    }


def get_fake_project_branch(ref=None, revision=None, can_delete=None):
    """Creates a random fake BranchInfo entry."""

    return {
        "ref": ref or "refs/heads/master",
        "revision": revision or "67ebf73496383c6777035e374d2d664009e2aa5c",
        "can_delete": can_delete or True,
        "web_links": [
            {u'url': u'gitweb?p=fake.git;a=shortlog;h=refs%2Fmeta%2Fconfig',
             u'name': u'gitweb'}
        ]
    }


def get_fake_project_branches(branch_count, **kwargs):
    """Creates a list of BranchInfo entries."""

    return [get_fake_project_branch(**kwargs) for _ in range(branch_count)]
