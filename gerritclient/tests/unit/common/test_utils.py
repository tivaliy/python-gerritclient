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

from oslotest import base as oslo_base

from gerritclient.common import utils


class TestUtils(oslo_base.BaseTestCase):

    def test_get_display_data_single(self):
        columns = ('id', 'name')
        data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(
            utils.get_display_data_single(fields=columns, data=data),
            [1, 'test_name']
        )

    def test_get_display_data_single_with_none_existent_field(self):
        columns = ('id', 'name', 'non-existent')
        data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(
            utils.get_display_data_single(fields=columns, data=data),
            [1, 'test_name', None]
        )

    def test_get_display_data_multi(self):
        columns = ('id', 'name')
        data = [{'id': 1, 'name': 'test_name_1'},
                {'id': 2, 'name': 'test_name_2'}]
        self.assertEqual(
            utils.get_display_data_multi(fields=columns, data=data),
            [[1, 'test_name_1'], [2, 'test_name_2']]
        )
