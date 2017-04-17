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

from gerritclient.tests.utils import fake_account


def get_fake_group(name="fake-group", group_id=1, is_single_item=True):
    """Creates a fake group

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    fake_group = {
        "id": "6a1e70e1a88782771a91808c8af9bbb7a9871389",
        "url": "#/admin/groups/uuid-6a1e70e1a88782771a91808c8af9bbb7a9871389",
        "options": {
            "visible_to_all": True
        },
        "description": "Fake group description",
        "group_id": group_id,
        "owner": "Fake Owner",
        "owner_id": "5057f3cbd3519d6ab69364429a89ffdffba50f73",
        "members": fake_account.get_fake_accounts(5),
        "includes": []
    }
    # 'name' key set only for single item, otherwise 'name' key is used
    # as map key if we try to fetch several items
    if is_single_item:
        fake_group['name'] = name
        return fake_group
    return {name: fake_group}


def get_fake_groups(groups_count):
    """Creates a random fake groups map."""

    fake_groups = {}
    for item in range(1, groups_count + 1):
        fake_groups.update(get_fake_group(name="fake-group-{0}".format(item),
                                          group_id=item,
                                          is_single_item=False))
    return fake_groups
