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
"""Intl models."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TranslationModel(models.Model):
    """Abstract model respresenting a translation."""

    language = models.CharField(
        max_length=16,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE,
        verbose_name=_('language'),
    )

    class Meta:
        abstract = True

    def get_all_translations(self):
        """Get a list of all translations ordered by language."""
        return list(self.parent.translations.order_by('language'))

    def get_other_translations(self):
        """Get a list of other translations ordered by language."""
        return list(self.parent.translations.exclude(id=self.id).order_by('language'))
