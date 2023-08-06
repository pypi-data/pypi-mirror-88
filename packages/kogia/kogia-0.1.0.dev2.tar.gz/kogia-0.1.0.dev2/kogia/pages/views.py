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
"""Pages views."""

from django.views.generic import DetailView, ListView


class PageDetail(DetailView):
    """View that displays a page."""

    context_object_name = 'page'
    template_name = 'pages/page_detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(language=self.request.LANGUAGE_CODE).select_related()


class PageList(ListView):
    """View that displays the list of pages."""

    context_object_name = 'page_list'
    template_name = 'pages/page_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(language=self.request.LANGUAGE_CODE).select_related()
