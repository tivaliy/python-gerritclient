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


def get_fake_change(change_id=None):
    """Creates a fake change."""

    return {
        "id": change_id or "I8473b95934b5732ac55d26311a706c9c2bde9940",
        "project": "myProject",
        "branch": "master",
        "change_id": "I8473b95934b5732ac55d26311a706c9c2bde9940",
        "subject": "Implementing Feature X",
        "status": "NEW",
        "created": "2017-07-26 09:59:32.126000000",
        "updated": "2013-07-27 11:16:36.775000000",
        "mergeable": True,
        "insertions": 34,
        "deletions": 101,
        "_number": 3965,
        "owner": {
            "name": "John Doe"
        }
    }
