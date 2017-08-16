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


def get_fake_change(identifier=None, project=None, branch=None,
                    subject=None, topic=None):
    """Creates a fake change."""

    return {
        "id": identifier or "myProject~master~"
                            "I8473b95934b5732ac55d26311a706c9c2bde9940",
        "project": project or "myProject",
        "branch": branch or "master",
        "topic": topic or "Feature X Topic",
        "change_id": "I8473b95934b5732ac55d26311a706c9c2bde9940",
        "subject": subject or "Implementing Feature X",
        "status": "NEW",
        "created": "2017-07-26 09:59:32.126000000",
        "updated": "2013-07-27 11:16:36.775000000",
        "mergeable": True,
        "insertions": 34,
        "deletions": 101,
        "_number": 3965,
        "owner": {
            "_account_id": 1000096,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "username": "jdoe"
        },
        "problems": [
            {
                "message": "Current patch set 1 not found"
            }
        ],
        "labels": {
            "Verified": {
                "all": [
                    {
                        "value": 0,
                        "_account_id": 1000096,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "username": "jdoe"
                    },
                    {
                        "value": 0,
                        "_account_id": 1000097,
                        "name": "Jane Roe",
                        "email": "jane.roe@example.com",
                        "username": "jroe"
                    }
                ],
                "values": {
                    "-1": "Fails",
                    " 0": "No score",
                    "+1": "Verified"
                }
            },
            "Code-Review": {
                "disliked": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "all": [
                    {
                        "value": -1,
                        "_account_id": 1000096,
                        "name": "John Doe",
                        "email": "john.doe@example.com",
                        "username": "jdoe"
                    },
                    {
                        "value": 1,
                        "_account_id": 1000097,
                        "name": "Jane Roe",
                        "email": "jane.roe@example.com",
                        "username": "jroe"
                    }
                ],
                "values": {
                    "-2": "This shall not be merged",
                    "-1": "I would prefer this is not merged as is",
                    " 0": "No score",
                    "+1": "Looks good to me, but someone else must approve",
                    "+2": "Looks good to me, approved"
                }
            }
        },
        "permitted_labels": {
            "Verified": [
                "-1",
                " 0",
                "+1"
            ],
            "Code-Review": [
                "-2",
                "-1",
                " 0",
                "+1",
                "+2"
            ]
        },
        "removable_reviewers": [
            {
                "_account_id": 1000096,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "username": "jdoe"
            },
            {
                "_account_id": 1000097,
                "name": "Jane Roe",
                "email": "jane.roe@example.com",
                "username": "jroe"
            }
        ],
        "reviewers": {
            "REVIEWER": [
                {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                {
                    "_account_id": 1000097,
                    "name": "Jane Roe",
                    "email": "jane.roe@example.com",
                    "username": "jroe"
                }
            ]
        },
        "reviewer_updates": [
            {
                "state": "REVIEWER",
                "reviewer": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated_by": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated": "2016-07-21 20:12:39.000000000"
            },
            {
                "state": "REMOVED",
                "reviewer": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated_by": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated": "2016-07-21 20:12:33.000000000"
            },
            {
                "state": "CC",
                "reviewer": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated_by": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated": "2016-03-23 21:34:02.419000000",
            },
        ],
        "messages": [
            {
                "id": "YH-egE",
                "author": {
                    "_account_id": 1000096,
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "username": "jdoe"
                },
                "updated": "2013-03-23 21:34:02.419000000",
                "message": "Patch Set 1:\n\nThis is the first message.",
                "revision_number": 1
            },
            {
                "id": "WEEdhU",
                "author": {
                    "_account_id": 1000097,
                    "name": "Jane Roe",
                    "email": "jane.roe@example.com",
                    "username": "jroe"
                },
                "updated": "2013-03-23 21:36:52.332000000",
                "message": "Patch Set 1:\n\nThis is the second message."
                           "\n\nWith a line break.",
                "revision_number": 1
            }
        ]
    }


def get_fake_changes(change_count, **kwargs):
    """Creates a random fake list of changes."""

    return [get_fake_change(**kwargs) for _ in range(change_count)]
