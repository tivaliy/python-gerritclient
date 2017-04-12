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


def get_fake_plugin(plugin_id="fake-plugin"):
    """Creates a fake plugin

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """

    return {
        "id": plugin_id,
        "version": "1.0",
        "index_url": "plugins/{0}/".format(plugin_id),
        "disabled": None
    }


def get_fake_plugins(plugins_count):
    """Creates a random fake plugins map."""

    fake_plugins = {}
    for i in range(1, plugins_count + 1):
        fake_plugins["fake-plugin-{}".format(i)] = \
            get_fake_plugin("fake-plugin-{}".format(i))
    return fake_plugins
