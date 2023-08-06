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
"""Tests for Pages views."""

from django.test import TestCase, modify_settings, override_settings
from django.urls import reverse

from kogia.pages.tests.models import Page, PageTranslation


class BasePageViewTest(TestCase):
    """Base class for testing Pages views."""

    @classmethod
    def setUpTestData(cls):
        """Create objects for all tests."""
        cls.page = Page.objects.create(title='Bar')
        cls.page_en = PageTranslation.objects.create(slug='bar', title='Bar', parent=cls.page,
                                                     language='en')


@modify_settings(INSTALLED_APPS={'prepend': 'kogia.pages.tests'})
@override_settings(ROOT_URLCONF='kogia.pages.tests.urls')
class PageDetailViewTest(BasePageViewTest):
    """Tests for the page detail view."""

    def test_route_from_name(self):
        page_detail_url = reverse('page-detail', kwargs={'slug': str(self.page_en.slug)})
        response = self.client.get(page_detail_url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_route_from_path(self):
        response = self.client.get(self.page_en.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_templates_used(self):
        response = self.client.get(self.page_en.get_absolute_url(), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/page_detail.html')


@modify_settings(INSTALLED_APPS={'prepend': 'kogia.pages.tests'})
@override_settings(ROOT_URLCONF='kogia.pages.tests.urls')
class PageListViewTest(BasePageViewTest):
    """Tests for the page list view."""

    def test_route_from_name(self):
        response = self.client.get(reverse('page-list'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_route_from_path(self):
        response = self.client.get('/pages/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_templates_used(self):
        response = self.client.get(reverse('page-list'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/page_list.html')
