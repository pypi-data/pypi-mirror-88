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
"""Tests for Pages models."""

from django.db.utils import IntegrityError
from django.test import TestCase, modify_settings, override_settings

from kogia.pages.tests.models import Page, PageTranslation


@modify_settings(INSTALLED_APPS={'prepend': 'kogia.pages.tests'})
@override_settings(ROOT_URLCONF='kogia.pages.tests.urls')
class PageModelTest(TestCase):
    """Tests for the page model."""

    @classmethod
    def setUpTestData(cls):
        """Create objects for all tests."""
        cls.page = Page.objects.create(title='Bar')

    def test_title_max_length(self):
        max_length = self.page._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_object_string_representation(self):
        self.assertEquals(str(self.page), self.page.title)


@modify_settings(INSTALLED_APPS={'prepend': 'kogia.pages.tests'})
@override_settings(ROOT_URLCONF='kogia.pages.tests.urls')
class PageTranslationModelTest(TestCase):
    """Tests for the page translation model."""

    @classmethod
    def setUpTestData(cls):
        """Create objects for all tests."""
        cls.page = Page.objects.create(title='Bar')
        cls.page_en = PageTranslation.objects.create(slug='bar', title='Bar', parent=cls.page,
                                                     language='en')

    def test_slug_max_length(self):
        max_length = self.page_en._meta.get_field('slug').max_length
        self.assertEquals(max_length, 255)

    def test_title_max_length(self):
        max_length = self.page_en._meta.get_field('title').max_length
        self.assertEquals(max_length, 255)

    def test_object_string_representation(self):
        self.assertEquals(str(self.page_en), self.page_en.title)

    def test_siblings_have_different_languages(self):
        with self.assertRaises(IntegrityError):
            PageTranslation.objects.create(slug='foo-bar', title='Foo Bar', parent=self.page,
                                           language='en')

    def test_slug_and_language_are_unique_together(self):
        with self.assertRaises(IntegrityError):
            page2 = Page.objects.create(title='Bar2')
            PageTranslation.objects.create(slug='bar', title='Bari', parent=page2, language='en')
