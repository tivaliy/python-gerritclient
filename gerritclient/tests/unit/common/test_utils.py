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

    def test_get_display_data_single_with_non_existent_field(self):
        columns = ('id', 'name', 'non-existent')
        data = {'id': 1, 'name': 'test_name'}
        self.assertEqual(
            utils.get_display_data_single(fields=columns, data=data),
            [1, 'test_name', None]
        )

    def test_get_display_data_multi_wo_sorting(self):
        columns = ('id', 'name')
        data = [{'id': 1, 'name': 'test_name_1'},
                {'id': 2, 'name': 'test_name_2'}]
        self.assertEqual(
            utils.get_display_data_multi(fields=columns, data=data),
            [[1, 'test_name_1'], [2, 'test_name_2']]
        )

    def test_get_display_data_multi_w_sorting(self):
        columns = ('id', 'name', 'severity_level')
        data = [{'id': 3, 'name': 'twitter', 'severity_level': 'error'},
                {'id': 15, 'name': 'google', 'severity_level': 'warning'},
                {'id': 2, 'name': 'amazon', 'severity_level': 'error'},
                {'id': 17, 'name': 'facebook', 'severity_level': 'note'}]
        # by single field
        self.assertEqual(
            utils.get_display_data_multi(fields=columns, data=data,
                                         sort_by=['name']),
            [[2, 'amazon', 'error'],
             [17, 'facebook', 'note'],
             [15, 'google', 'warning'],
             [3, 'twitter', 'error']]
        )
        # by multiple fields
        self.assertEqual(
            utils.get_display_data_multi(fields=columns, data=data,
                                         sort_by=['severity_level', 'id']),
            [[2, 'amazon', 'error'],
             [3, 'twitter', 'error'],
             [17, 'facebook', 'note'],
             [15, 'google', 'warning']]
        )
