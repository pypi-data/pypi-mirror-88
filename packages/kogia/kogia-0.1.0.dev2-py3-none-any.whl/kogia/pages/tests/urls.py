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
"""URL configuration for testing the Pages application."""

from django.urls import path

from kogia.pages.tests import views

urlpatterns = [
    path('pages/<slug:slug>/', views.PageDetail.as_view(), name='page-detail'),
    path('pages/', views.PageList.as_view(), name='page-list'),
]
