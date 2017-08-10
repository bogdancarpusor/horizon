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

from collections import OrderedDict
from gnocchiclient import auth
from gnocchiclient.v1 import client
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base
from openstack_dashboard.api import keystone

from horizon import exceptions
from keystoneauth1.identity.v3 import token
from constants import METRICS_DESCRIPTION
import test_values
import pdb
@memoized
def gnocchi_client(request):
    """Initialize Gnocchi client."""

    # TODO(Bogdan) - Set additional configuration for ssl
    endpoint = base.url_for(request, 'metric')
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', True)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', True)
    user = request.user
    roles = 'default'
    auth_plugin = GnocchiTokenNoAuthPlugin(user.token.id,
                                           endpoint,
                                           project_id=user.project_id,
                                           user_id=user.id)

    return client.Client(session_options={'auth': auth_plugin})


class GnocchiTokenNoAuthPlugin(auth.GnocchiNoAuthPlugin):
    """No authentication plugin that makes use of the user token
    """
    def __init__(self, token_id, endpoint, **kwargs):
        user_id = kwargs.get('user_id', 'None')
        project_id = kwargs.get('project_id', 'None')
        roles = kwargs.get('roles', 'None')
        super(GnocchiTokenNoAuthPlugin, self).__init__(user_id, project_id,
                                                       roles, endpoint)
        self._token = token_id

    def get_headers(self, session, **kwargs):
        return {'x-user-id': self._user_id,
                'x-auth-token': self._token,
                'x-project-id': self._project_id
                }

    def get_token(self, session, **kwargs):
        return self._token


def is_iterable(var):
    """Return True if the given is list or tuple."""

    return (isinstance(var, (list, tuple)) or
            issubclass(var.__class__, (list, tuple)))


class Meter(base.APIResourceWrapper):
    _attrs = ['id', 'name', 'unit', 'creator', "resource_id"]

    def __init__(self, apiresource):
        super(Meter, self).__init__(apiresource)
        self._description = METRICS_DESCRIPTION.get(self._name, '')

    def augment(self, label=None, description=None):
        if label:
            self._label = label
        if description:
            self._description = description

    @property
    def name(self):
        return self._apiresource.get('name', None)

    @property
    def unit(self):
        return self._apiresource.get('unit', None)

    @property
    def id(self):
        return self._apiresource.get('id', None)

    @property
    def description(self):
        return self._description

    @property
    def resource_id(self):
        return self._apiresource.get('resource_id', None)

    @staticmethod
    def find_and_create(client, meter_id):
        return Meter(client.metric.get(meter_id))


class ResourceType(base.APIResourceWrapper):
    _attrs = ['name', 'state']

    def __init__(self, apiresource):
        super(ResourceType, self).__init__(apiresource)

    @property
    def name(self):
        return self._apiresource.get('name', None)

    @property
    def state(self):
        return self._apiresource.get('state', None)

    @staticmethod
    def list_resource_types(gnocchiclient):
        return gnocchiclient.resource_type.list()

    @staticmethod
    def init_resource_types(gnocchiclient):
        resource_types = ResourceType.list_resource_types(gnocchiclient)
        return [ResourceType(res_type) for res_type in test_values.RESOURCE_TYPES if str(res_type['state']) == 'active']
            
class Resource(base.APIResourceWrapper):
    _attrs = ['id', 'type', 'display_name', 'source', 'metadata', 'user_id', 'project_id']

    def __init__(self, apiresource, gnocchiclient):
        super(Resource, self).__init__(apiresource)
        self.metrics = []
        for meter_name, meter_id in apiresource['metrics'].items():
            self.metrics.append({'name': meter_name, 'id': meter_id})
        #for meter_name, meter_id in apiresource['metrics'].items():
        #    self.meters[meter_name] = Meter.find_and_create(gnocchiclient, meter_id)

    @property
    def name(self):
        name = self._apiresource.get('name', None)
        display_name = self.metadata.get("display_name", None)
        return name or display_name or self.id

    @property
    def source(self):
        return self._apiresource.get('source', None)

    @property
    def type(self):
        return self._apiresource.get('type', None)

    @property
    def metadata(self):
        return self._apiresource.get('metadata', {})

    @property
    def project(self):
        return self._apiresource.get('project_id', None)
   
    @property
    def id(self):
        return self._apiresource.get('id', None)

    @property
    def tenant(self):
        return self._apiresource.get('tenant', None)

    @property
    def user_id(self):
        return self._apiresource.get('user_id', None)

    @staticmethod
    def get_resource(gnocchiclient, resource_type, resource_id):
        return gnocchi_client.resource.get(resource_type, resource_id)

    @staticmethod
    def list_resource(gnocchiclient, resource_type='generic'):
        return gnocchiclient.resource.list(resource_type)

    @staticmethod
    def init_resources(gnocchiclient, resource_types, project_id):
        # TODO(Bogdan): Should use search instead of list. Need to find out
        # how querying works for the gnocchi client
        resources_list = []        
        
        for resource_type in resource_types:
            #resources = gnocchiclient.resource.list(resource_type)
            resources = test_values.RESOURCES.get(resource_type, [])
            if not resources:
                pass
            else:
                for resource in resources:
                    if str(resource['project_id']) == test_values.PROJECT_ID:
                        resources_list.append(Resource(resource, gnocchiclient))

        return resources_list

    def get_metrics(self, *args):
        for metric in self.metrics:
            return {
                'id': metric['id'],
                'meter': metric['name'],
                'resource': self.name,
                'project': self.project,
                'project_id': self.project,
                'description': METRICS_DESCRIPTION.get(metric['name'], ''),
                'unit': ''
            }

    def get_meter(self, meter_name):
        return self.meters.get(meter_name, '')

    def set_meter(self, meter_name, value):
        self._meters[meter_name] = value