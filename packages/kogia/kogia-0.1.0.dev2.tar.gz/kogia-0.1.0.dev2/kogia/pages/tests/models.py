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
"""Models for testing the Pages application."""

from django.db import models
from django.urls import reverse

from kogia.pages.models import AbstractPage, AbstractPageTranslation


class Page(AbstractPage):
    """Test model representing a page."""


class PageTranslation(AbstractPageTranslation):
    """Test model representing a page translation."""

    parent = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='translations',
    )

    class Meta:
        ordering = ['parent', 'language']
        unique_together = [
            ['parent', 'language'],
            ['slug', 'language'],
        ]

    def get_absolute_url(self):
        return reverse('page-detail', kwargs={'slug': str(self.slug)})
