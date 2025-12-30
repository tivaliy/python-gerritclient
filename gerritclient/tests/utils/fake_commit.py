#
#    Copyright 2018 Vitalii Kulanov
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


def get_fake_commit(commit_id=None):
    return {
        "commit": commit_id or "184ebe53805e102605d11f6b143486d15c23a09c",
        "parents": [
            {
                "commit": "1eee2c9d8f352483781e772f35dc586a69ff5646",
                "subject": "Migrate contributor agreements to All-Projects.",
            }
        ],
        "author": {
            "name": "Shawn O. Pearce",
            "email": "sop@google.com",
            "date": "2012-04-24 18:08:08.000000000",
            "tz": -420,
        },
        "committer": {
            "name": "Shawn O. Pearce",
            "email": "sop@google.com",
            "date": "2012-04-24 18:08:08.000000000",
            "tz": -420,
        },
        "subject": "Use an EventBus to manage star icons",
        "message": "Use an EventBus to manage star icons\n\n"
        "Image widgets that need to ...",
    }


def get_fake_commit_affiliation():
    return {"branches": ["master", "fake/branch"], "tags": ["fake_tag"]}
