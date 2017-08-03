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

from openstack_dashboard.dashboards.admin.metrics import \
    tables as metrics_tables

class StatsTab(tabs.TableTab):
    name = _("Stats")
    slug = "stats"
    template_name = "admin/metrics/stats.html"
    preload = False
    table_classes = (metrics_tables.UsageTable,)

    def get_context_data(self, request):
        return {'test': 'test'}

class ReportsTab(tabs.Tab):
    name = _("Reports")
    slug = "reports"
    template_name = "admin/metrics/report.html"
    table_classes = (metrics_tables.UsageTable, )

    def get_context_data(self, request):
        return {'test': 'test'}


class MetricsTabs(tabs.TabGroup):
    slug = "metrics"
    tabs = (StatsTab, ReportsTab,)
    sticky = True
