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


def get_fake_weblinkinfo(name="gitweb",
                         project_id="fake-project"):
    """Creates a fake WebLinkInfo entity

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review WebLinkInfo entity.
    """
    return [
        {
            "name": name,
            "url": "gitweb?p\u003d{}.git;a\u003dsummary".format(project_id),
            "image_url": None
        }
    ]
