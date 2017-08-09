#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.contrib.humanize.templatetags import humanize
from django.utils import text
from django.utils.translation import ugettext_lazy as _

from django.utils.translation import pgettext_lazy
import six
from workflow import gnocchi_client
from django import forms as django_forms
from horizon import tables
from horizon import forms
import pdb

def show_date(datum):
    return datum.split('T')[0]

class GetMetricsValuesAction(tables.LinkAction):
    name = 'get_metrics_values'
    verbose_name = 'Get Metrics Values'
    url = "horizon:admin:metrics"
    icon = "plus"

class ResourceTypeAction(tables.LinkAction):
    name = 'get_resource_type'
    verbose_name = 'Resource Type'
    classes = ("ajax-modal",)
    url = "horizon:admin:metrics:resource_type"
    icon = "chevron-down"

class ResourcesAction(tables.LinkAction):
    name = 'get_resources'
    verbose_name = 'Resources'
    url = "horizon:admin:metrics"
    icon = "chevron-down"

class CreateChartAction(tables.LinkAction):
    name = 'create_chart'
    verbose_name = 'Create Chart'
    url = "horizon:admin:metrics"
    icon = "triangle-right"

class MetricFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (("name", _("Metric Name ="), True),
                        ("id", _("Metric ID ="), True),
                        ("resource", _("Resource ="), True),
                        ("project", _("Project =")))


class ValuesTable(tables.DataTable):
    id = tables.Column('id', verbose_name=_('Metric ID'),
                       attrs={'data-type': 'uuid'})
    resource = tables.Column('resource', verbose_name=_('Resource'))
    meter = tables.Column('meter', verbose_name=_('Meter'))
    time = tables.Column('time', verbose_name=_('Time'),
                         filters=[show_date])
    value = tables.Column('value', verbose_name=_('Value (Avg)'),
                          filters=[humanize.intcomma])
    unit = tables.Column('unit', verbose_name=_('Unit'))

    def get_object_id(self, metric):
        return '0'

    class Meta(object):
        name = 'values_table'
        verbose_name = _("Values")
        multi_select = True
        table_actions = (CreateChartAction, )


class UsageTable(tables.DataTable):
    STATUS_CHOICES = (
        ("min", True),
        ("max", False),
        ("medium", True),
    )

    STATUS_DISPLAY_CHOICES = (
        ("enabled", pgettext_lazy("Current status of a Hypervisor",
                                  u"Enabled")),
        ("disabled", pgettext_lazy("Current status of a Hypervisor",
                                   u"Disabled")),
        ("up", pgettext_lazy("Current state of a Hypervisor",
                             u"Up")),
        ("down", pgettext_lazy("Current state of a Hypervisor",
                               u"Down")),
    )

    id = tables.Column('id', verbose_name=_('ID'),
                       attrs={'data-type': 'uuid'})
    meter = tables.Column('meter', verbose_name=_('Name'))
    resource = tables.Column('resource', verbose_name=_('Resource'))
    project = tables.Column('project', verbose_name=_('Project'))
    description = tables.Column('description',
                                verbose_name=_('Description'),
                                display_choices=(('0', 0), ('1', 2)),
                                form_field=django_forms.ChoiceField)
    aggregation = tables.Column('aggregation',
                                verbose_name=_('Aggregation'),
                                form_field=forms.ChoiceField
                                )
    unit = tables.Column('unit', verbose_name=_('Unit'))

    def get_object_id(self, metric):
        return metric['id']
    
    class Meta(object):
        name = 'usage_table'
        verbose_name = _("Usage Report")
        table_actions = (ResourceTypeAction, ResourcesAction,
                         GetMetricsValuesAction, MetricFilterAction) 
        #                 SelectResourceTypeAction, SelectResourceAction)
        multi_select = True
        table_actions_template = 'admin/metrics/table_actions.html'
