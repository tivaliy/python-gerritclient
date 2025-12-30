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


def get_fake_tag():
    """Creates a fake TagInfo."""

    return {
        "ref": "refs/tags/v1.0",
        "revision": "49ce77fdcfd3398dc0dedbe016d1a425fd52d666",
        "object": "1624f5af8ae89148d1a3730df8c290413e3dcf30",
        "message": "Annotated tag",
        "tagger": {
            "name": "John Doe",
            "email": "j.doe@example.com",
            "date": "2014-10-06 07:35:03.000000000",
            "tz": 540,
        },
    }


def get_fake_tags(tags_count):
    """Creates a random fake tag list of a project."""

    return [get_fake_tag() for _ in range(tags_count)]
