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


def get_fake_comment(patch_set=None, comment_id=None, line=None, message=None,
                     author=None):
    """Creates a fake comment."""

    return {
        "patch_set": patch_set or 1,
        "id": comment_id or "TvcXrmjM",
        "line": line or 23,
        "message": message or "[nit] trailing whitespace",
        "updated": "2013-02-26 15:40:43.986000000",
        "author": author or {
            "_account_id": 1000096,
            "name": "John Doe",
            "email": "john.doe@example.com"
            }
        }


def get_fake_comments(comment_count, **kwargs):
    """Creates a random fake list of comments."""

    return [get_fake_comment(**kwargs) for _ in range(comment_count)]


def get_fake_comments_in_change(comment_count, path=None, **kwargs):
    """Creates a random fake list of comments in change."""

    return {
        path or "gerrit-server/fake/path/to/file":
            get_fake_comments(comment_count, **kwargs)
    }
