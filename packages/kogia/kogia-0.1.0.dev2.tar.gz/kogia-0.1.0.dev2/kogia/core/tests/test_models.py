# Copyright (C) 2017-2020 Pascal Pepe <contact@pascalpepe.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for Core models."""

from django.test import TestCase, modify_settings

from kogia.core.tests.models import AllCore


@modify_settings(INSTALLED_APPS={'prepend': 'kogia.core.tests'})
class AllCoreModelsTest(TestCase):
    """Tests for all core models."""

    @classmethod
    def setUpTestData(cls):
        """Create objects for all tests."""
        cls.allcore = AllCore.objects.create()

    def test_pub_status_max_length(self):
        max_length = self.allcore._meta.get_field('pub_status').max_length
        self.assertEquals(max_length, 32)

    def test_search_description_max_length(self):
        max_length = self.allcore._meta.get_field('search_description').max_length
        self.assertEquals(max_length, 255)

    def test_search_title_max_length(self):
        max_length = self.allcore._meta.get_field('search_title').max_length
        self.assertEquals(max_length, 255)

    def test_visibility_status_max_length(self):
        max_length = self.allcore._meta.get_field('visibility_status').max_length
        self.assertEquals(max_length, 32)
