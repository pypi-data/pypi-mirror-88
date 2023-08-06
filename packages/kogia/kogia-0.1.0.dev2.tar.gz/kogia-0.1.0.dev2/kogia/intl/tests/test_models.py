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
"""Tests for Intl models."""

from django.db.utils import IntegrityError
from django.test import TestCase, modify_settings

from kogia.intl.tests.models import Parent, Translation


@modify_settings(LOCAL_APPS={'prepend': 'kogia.intl.tests'})
class TranslationModelTest(TestCase):
    """Tests for the translation model."""

    @classmethod
    def setUpTestData(cls):
        """Create objects for all tests."""
        cls.parent = Parent.objects.create(pk=1)
        cls.translation_en = Translation.objects.create(parent=cls.parent, language='en')
        cls.translation_fr = Translation.objects.create(parent=cls.parent, language='fr')

    def test_language_max_length(self):
        max_length = self.translation_en._meta.get_field('language').max_length
        self.assertEquals(max_length, 16)

    def test_get_all_translations(self):
        self.assertEqual(self.translation_en.get_all_translations(),
                         list([self.translation_en, self.translation_fr]))

    def test_get_other_translations(self):
        self.assertEqual(self.translation_en.get_other_translations(),
                         list([self.translation_fr]))

    def test_siblings_have_different_languages(self):
        with self.assertRaises(IntegrityError):
            Translation.objects.create(parent=self.parent, language='fr')
