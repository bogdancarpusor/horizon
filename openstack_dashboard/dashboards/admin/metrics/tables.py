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
import six

from horizon import tables


def show_date(datum):
    return datum.split('T')[0]

class UsageTable(tables.DataTable):
    project = tables.Column('project', verbose_name=_('Project'))
    service = tables.Column('service', verbose_name=_('Service'))
    meter = tables.Column('meter', verbose_name=_('Meter'))
    description = tables.Column('description', verbose_name=_('Description'))
    time = tables.Column('time', verbose_name=_('Day'),
                         filters=[show_date])
    value = tables.Column('value', verbose_name=_('Value (Avg)'),
                          filters=[humanize.intcomma])
    unit = tables.Column('unit', verbose_name=_('Unit'))

    class Meta(object):
        name = 'usage_table'
        verbose_name = _("Usage Report")
        table_actions = ()
        multi_select = False
