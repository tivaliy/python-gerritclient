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


def get_fake_project(project_id=None,
                     name=None,
                     state=None,
                     parent=None,
                     is_weblinkinfo=True,
                     is_single_item=True):
    """Creates a fake project

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    fake_project = {
        "id": project_id or "fakes%2Ffake-project",
        "parent": parent or "Fake-Projects",
        "description": "{project_name} description".format(project_name=name),
        "state": state or "ACTIVE",
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
        fake_project['name'] = name or "fakes/fake-project"
        return fake_project
    return {name: fake_project}


def get_fake_projects(projects_count, is_weblinkinfo=True):
    """Creates a random fake projects map."""

    fake_projects = {}
    for item in range(1, projects_count + 1):
        fake_projects.update(
            get_fake_project(project_id="fakes%2project-{0}".format(item),
                             name="fakes/project-{0}".format(item),
                             is_single_item=False,
                             is_weblinkinfo=is_weblinkinfo)
        )
    return fake_projects


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


def get_fake_reflog(old_id=None, new_id=None, who=None, comment=None):
    """Creates a random fake ReflogEntryInfo entity."""

    return {
        "old_id": old_id or "976ced8f4fc0909d7e1584d18455299545881d60",
        "new_id": new_id or "2eaa94bac536654eb592c941e33b91f925698d16",
        "who": who or {
            "name": "Jane Roe",
            "email": "jane.roe@example.com",
            "date": "2014-06-30 11:53:43.000000000",
            "tz": 120
        },
        "comment": comment or "merged: fast forward"
    }


def get_fake_config(name=None):
    """Creates a random fake ConfigInfo entry."""

    return {
        "description": name or "demo project",
        "use_contributor_agreements": {
            "value": True,
            "configured_value": "TRUE",
            "inherited_value": False
        },
        "use_content_merge": {
            "value": True,
            "configured_value": "INHERIT",
            "inherited_value": True
        },
        "use_signed_off_by": {
            "value": False,
            "configured_value": "INHERIT",
            "inherited_value": False
        },
        "create_new_change_for_all_not_in_target": {
            "value": False,
            "configured_value": "INHERIT",
            "inherited_value": False
        },
        "require_change_id": {
            "value": False,
            "configured_value": "FALSE",
            "inherited_value": True
        },
        "max_object_size_limit": {
            "value": "15m",
            "configured_value": "15m",
            "inherited_value": "20m"
        },
        "submit_type": "MERGE_IF_NECESSARY",
        "state": "ACTIVE",
        "commentlinks": {},
        "plugin_config": {
            "helloworld": {
                "language": {
                    "display_name": "Preferred Language",
                    "type": "STRING",
                    "value": "en"
                }
            }
        },
        "actions": {
            "cookbook~hello-project": {
                "method": "POST",
                "label": "Say hello",
                "title": "Say hello in different languages",
                "enabled": True
            }
        }
    }
