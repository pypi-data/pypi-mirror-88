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
"""Core models."""

import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ArchivableModel(models.Model):
    """Abstract model that can be archived."""

    is_archived = models.BooleanField(
        default=False,
        verbose_name=_('archived?'),
    )

    class Meta:
        abstract = True


class OrderableModel(models.Model):
    """Abstract model that can be ordered."""

    order = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('order'),
    )

    class Meta:
        abstract = True


class OwnableModel(models.Model):
    """Abstract model with an optional owner."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('owner'),
    )

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """Abstract model with publication features."""

    PUB_STATUS_CHOICES = [
        ('DRAFT', _('draft')),
        ('PENDING', _('pending')),
        ('PUBLISHED', _('published')),
    ]

    pub_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('publication date'),
    )
    pub_status = models.CharField(
        max_length=32,
        choices=PUB_STATUS_CHOICES,
        default='DRAFT',
        verbose_name=_('publication status'),
    )

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract model with SEO-specific fields."""

    search_title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('search title'),
    )
    search_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('search description'),
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract model with a UUID as primary key."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
    )

    class Meta:
        abstract = True


class VisibilityStatusModel(models.Model):
    """Abstract model with a visibility status."""

    VISIBILITY_STATUS_CHOICES = [
        ('PRIVATE', _('private')),
        ('PUBLIC', _('public')),
    ]

    visibility_status = models.CharField(
        max_length=32,
        choices=VISIBILITY_STATUS_CHOICES,
        default='PUBLIC',
        verbose_name=_('visibility status'),
    )

    class Meta:
        abstract = True
