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
"""Pages models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from kogia.core.models import SEOModel, VisibilityStatusModel
from kogia.intl.models import TranslationModel


class AbstractPage(VisibilityStatusModel):
    """Abstract model representing the base of a page."""

    title = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class AbstractPageTranslation(SEOModel, TranslationModel):
    """Abstract model representing the base of a page translation."""

    slug = models.SlugField(
        max_length=255,
        verbose_name=_('slug'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )
    content = models.TextField(
        blank=True,
        verbose_name=_('content'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
