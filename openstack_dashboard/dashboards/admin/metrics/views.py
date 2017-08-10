# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse  # noqa
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import django.views

from horizon import exceptions
from horizon import forms
from horizon import tabs
from horizon import workflows
import workflows as metrics_workflows
from gnocchi import gnocchi_client, ResourceType

from openstack_dashboard.dashboards.admin.metrics import tabs as \
    metrics_tabs
from openstack_dashboard.dashboards.admin.metrics import forms as \
    metrics_forms
import pdb

class IndexView(tabs.TabbedTableView):
    tab_group_class = metrics_tabs.MetricsTabs
    template_name = 'admin/metrics/index.html'
    page_title = _("Resources Usage Overview")

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
      
        context['form'] = self.get_form(self.request)
        return context

    def get_form(self, request):
        if not hasattr(self, 'form'):
            req = request
            start = req.GET.get('start', req.session.get('usage_start'))
            end = req.GET.get('end', req.session.get('usage_end'))
            if start and end:
                # bound form
                self.form = forms.DateForm({'start': start, 'end': end})
            else:
                # non-bound form
                start_time = timezone.now() - timezone.timedelta(days=1)
                end_time = timezone.now()
                start = start_time.isoformat()
                end = end_time.isoformat()
                self.form = forms.DateForm(initial={'start': start,
                                                    'end': end})
            req.session['gnocchi']['usage_start'] = start
            req.session.modified = True
            req.session['gnocchi']['usage_end'] = end
            req.session.modified = True
            pdb.set_trace()
        return self.form

class ResourceTypeView(workflows.WorkflowView):
    workflow_class = metrics_workflows.SelectResourceType
    template_name = "admin/metrics/select_resource_type.html"
    page_title = _("Resource Types")

class ResourceView(workflows.WorkflowView):
    workflow_class = metrics_workflows.SelectResource
    template_name = "admin/metrics/select_resource.html"
    page_title = _("Resources")