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


from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import messages
from horizon import tabs
from gnocchi import gnocchi_client, ResourceType, Resource, Meter
from openstack_dashboard.dashboards.admin.metrics import \
    tables as metrics_tables

import test_values
import pdb



class StatsTab(tabs.TableTab):
    name = _("Metrics")
    slug = "stats"
    template_name = "horizon/common/_detail_table.html"
    table_classes = (metrics_tables.UsageTable,)

    def get_metrics(self, resources):
        metrics = []
        # try:
        client = gnocchi_client(self.request)
        for resource in resources:
            resource_id, resource_type = resource.split("?=")
            #resource_obj = client.resource.get(resource[1], resource[0])
            for name, value in test_values.RESOURCES.items():
                if name == resource_type:
                    for resource_value in value:
                        if resource_id == str(resource_value['id']):
                            resource_obj = Resource(resource_value, client)
                            m_list = resource_obj.get_metrics()
                            metrics.append(m_list)
        # except Exception:
        #     exceptions.handle(self.request,
        #                           _('Unable to retrieve metrics information.'))
        return metrics

    def get_usage_table_data(self):
        metrics = []
        metrics_session = self.request.session.get('gnocchi', {})
        resources = metrics_session.get('resources', [])
        pdb.set_trace()
        if not metrics_session:
            self.request.session['gnocchi'] = {}
            self.request.session.modified = True
            metrics = []
        elif not resources:
            metrics = []
        else:
            metrics = self.get_metrics(resources)
        return metrics

class MetricsValuesTab(tabs.TableTab):
    name = _("Metrics Values")
    slug = "values"
    template_name = "horizon/common/_detail_table.html"
    table_classes = (metrics_tables.ValuesTable,)

    def get_values_table_data(self):
        metric_ids = self.request.session['gnocchi'].get('metric_values', [])
        metric_ids = []
        if not metric_ids:
            return []
        else:
            client = gnocchi_client(self.request)
            start_date = self.request.session['gnocchi'].get('usage_start', '')
            end_date = self.request.session['gnocchi'].get('usage_end', '')
            metric_values = client.metric.aggregation(metric_ids, start=start_date, stop=end_date)
            

class MetricsTabs(tabs.TabGroup):
    slug = "metrics"
    tabs = (StatsTab, MetricsValuesTab, )
    sticky = True