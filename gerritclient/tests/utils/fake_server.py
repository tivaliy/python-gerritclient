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


def get_fake_config():
    """Creates a fake Gerrit server configuration.

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "auth": {
            "auth_type": "LDAP",
            "use_contributor_agreements": True,
            "contributor_agreements": [
                {
                    "name": "Individual",
                    "description": "If you are going to be contributing code "
                                   "on your own, this is the one you want. "
                                   "You can sign this one online.",
                    "url": "static/cla_individual.html"
                }
            ],
            "editable_account_fields": [
                "FULL_NAME",
                "REGISTER_NEW_EMAIL"
            ]
        },
        "download": {
            "schemes": {
                "anonymous http": {
                    "url": "http://gerrithost:8080/${project}",
                    "commands": {
                        "Checkout":
                            "git fetch http://gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git checkout FETCH_HEAD",
                        "Format Patch":
                            "git fetch http://gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git format-patch -1 "
                            "--stdout FETCH_HEAD",
                        "Pull":
                            "git pull http://gerrithost:8080/${project} "
                            "${ref}",
                        "Cherry Pick":
                            "git fetch http://gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git cherry-pick FETCH_HEAD"
                    },
                    "clone_commands": {
                        "Clone": "git clone http://gerrithost:8080/${project}",
                        "Clone with commit-msg hook":
                            "git clone http://gerrithost:8080/${project} "
                            "\u0026\u0026 scp -p -P 29418 "
                            "jdoe@gerrithost:hooks/commit-msg "
                            "${project}/.git/hooks/"
                    }
                },
                "http": {
                    "url": "http://jdoe@gerrithost:8080/${project}",
                    "is_auth_required": True,
                    "is_auth_supported": True,
                    "commands": {
                        "Checkout":
                            "git fetch http://jdoe@gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git checkout FETCH_HEAD",
                        "Format Patch":
                            "git fetch http://jdoe@gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git format-patch -1 "
                            "--stdout FETCH_HEAD",
                        "Pull":
                            "git pull http://jdoe@gerrithost:8080/${project} "
                            "${ref}",
                        "Cherry Pick":
                            "git fetch http://jdoe@gerrithost:8080/${project} "
                            "${ref} \u0026\u0026 git cherry-pick FETCH_HEAD"
                    },
                    "clone_commands": {
                        "Clone":
                            "git clone http://jdoe@gerrithost:8080/${project}",
                        "Clone with commit-msg hook":
                            "git clone http://jdoe@gerrithost:8080/${project} "
                            "\u0026\u0026 scp -p -P 29418 "
                            "jdoe@gerrithost:hooks/commit-msg "
                            "${project}/.git/hooks/"
                    }
                },
                "ssh": {
                    "url": "ssh://jdoe@gerrithost:29418/${project}",
                    "is_auth_required": True,
                    "is_auth_supported": True,
                    "commands": {
                        "Checkout":
                            "git fetch ssh://jdoe@gerrithost:29418/${project} "
                            "${ref} \u0026\u0026 git checkout FETCH_HEAD",
                        "Format Patch":
                            "git fetch ssh://jdoe@gerrithost:29418/${project} "
                            "${ref} \u0026\u0026 git format-patch -1 "
                            "--stdout FETCH_HEAD",
                        "Pull":
                            "git pull ssh://jdoe@gerrithost:29418/${project} "
                            "${ref}",
                        "Cherry Pick":
                            "git fetch ssh://jdoe@gerrithost:29418/${project} "
                            "${ref} \u0026\u0026 git cherry-pick FETCH_HEAD"
                    },
                    "clone_commands": {
                        "Clone":
                            "git clone ssh://jdoe@gerrithost:29418/${project}",
                        "Clone with commit-msg hook":
                            "git clone ssh://jdoe@gerrithost:29418/${project} "
                            "\u0026\u0026 scp -p -P 29418 "
                            "jdoe@gerrithost:hooks/commit-msg "
                            "${project}/.git/hooks/"
                    }
                }
            },
            "archives": [
                "tgz",
                "tar",
                "tbz2",
                "txz"
            ]
        },
        "gerrit": {
            "all_projects": "All-Projects",
            "all_users": "All-Users",
            "doc_search": True,
            "web_uis": ["gwt"]
        },
        "sshd": {},
        "suggest": {
            "from": 0
        },
        "user": {
            "anonymous_coward_name": "Anonymous Coward"
        }
    }


def get_fake_capabilities():
    """Creates a fake capabilities data.

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "accessDatabase": {
            "id": "accessDatabase",
            "name": "Access Database"
        },
        "administrateServer": {
            "id": "administrateServer",
            "name": "Administrate Server"
        },
        "createAccount": {
            "id": "createAccount",
            "name": "Create Account"
        },
        "createGroup": {
            "id": "createGroup",
            "name": "Create Group"
        },
        "createProject": {
            "id": "createProject",
            "name": "Create Project"
        },
        "emailReviewers": {
            "id": "emailReviewers",
            "name": "Email Reviewers"
        },
        "flushCaches": {
            "id": "flushCaches",
            "name": "Flush Caches"
        },
        "killTask": {
            "id": "killTask",
            "name": "Kill Task"
        },
        "priority": {
            "id": "priority",
            "name": "Priority"
        },
        "queryLimit": {
            "id": "queryLimit",
            "name": "Query Limit"
        },
        "runGC": {
            "id": "runGC",
            "name": "Run Garbage Collection"
        },
        "streamEvents": {
            "id": "streamEvents",
            "name": "Stream Events"
        },
        "viewCaches": {
            "id": "viewCaches",
            "name": "View Caches"
        },
        "viewConnections": {
            "id": "viewConnections",
            "name": "View Connections"
        },
        "viewPlugins": {
            "id": "viewPlugins",
            "name": "View Plugins"
        },
        "viewQueue": {
            "id": "viewQueue",
            "name": "View Queue"
        }
    }


def get_fake_caches_info():
    """Creates a fake caches info data.

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """
    return {
        "accounts": {
            "type": "MEM",
            "entries": {
                "mem": 4
            },
            "average_get": "2.5ms",
            "hit_ratio": {
                "mem": 94
            }
        },
        "accounts_byemail": {
            "type": "MEM",
            "entries": {
                "mem": 4
            },
            "average_get": "771.8us",
            "hit_ratio": {
                "mem": 95
            }
        },
        "accounts_byname": {
            "type": "MEM",
            "entries": {
                "mem": 4
            },
            "hit_ratio": {
                "mem": 100
            }
        },
        "adv_bases": {
            "type": "MEM",
            "entries": {},
            "hit_ratio": {}
        },
        "change_kind": {
            "type": "DISK",
            "entries": {
                "space": "0.00k"
            },
            "hit_ratio": {}
        },
        "changes": {
            "type": "MEM",
            "entries": {},
            "hit_ratio": {}
        },
        "conflicts": {
            "type": "DISK",
            "entries": {
                "mem": 2,
                "disk": 3,
                "space": "2.75k"
            },
            "hit_ratio": {
                "mem": 0,
                "disk": 100
            }
        },
        "diff": {
            "type": "DISK",
            "entries": {
                "mem": 177,
                "disk": 253,
                "space": "170.97k"
            },
            "average_get": "1.1ms",
            "hit_ratio": {
                "mem": 67,
                "disk": 100
            }
        },
        "diff_intraline": {
            "type": "DISK",
            "entries": {
                "mem": 1,
                "disk": 1,
                "space": "0.37k"
            },
            "average_get": "6.8ms",
            "hit_ratio": {
                "mem": 0
            }
        },
        "git_tags": {
            "type": "DISK",
            "entries": {
                "space": "0.00k"
            },
            "hit_ratio": {}
        }
    }
