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
import threading

from gnocchiclient import auth
from gnocchiclient.v1 import client
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon.utils.memoized import memoized  # noqa

from openstack_dashboard.api import base
from openstack_dashboard.api import keystone

from keystoneauth1.identity.v3 import token


@memoized
def gnocchi_client(request):
    """Initialize Gnocchi client."""

    endpoint = base.url_for(request, 'metric')
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', True)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', True)
    user = request.user
    roles = 'default'
    auth_plugin = GnocchiTokenNoAuthPlugin(user.token.id,
                                           endpoint,
                                           project_id=user.project_id)

    return client.Client(session_options={'auth': auth_plugin,
                                          'cert': cacert})


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

    _metrics_description = {
        "instance": _("Existence of instance"),
        "instance:<type>": _("Existence of instance <type> "),
        "memory": _("Volume of RAM"),
        "memory.usage": _("Volume of RAM used"),
        "cpu": _("CPU time used"),
        "cpu_util": _("Average CPU utilization"),
        "vcpus": _("Number of VCPUs"),
        "disk.read.requests": _("Number of read requests"),
        "disk.write.requests": _("Number of write requests"),
        "disk.read.bytes": _("Volume of reads"),
        "disk.write.bytes": _("Volume of writes"),
        "disk.read.requests.rate": _("Average rate of read requests"),
        "disk.write.requests.rate": _("Average rate of write requests"),
        "disk.read.bytes.rate": _("Average rate of reads"),
        "disk.write.bytes.rate":_( "Average volume of writes"),
        "disk.root.size": _("Size of root disk"),
        "disk.ephemeral.size": _("Size of ephemeral disk"),
        "network.incoming.bytes": _("Number of incoming bytes "
                                    "on the network for a VM interface"),
        "network.outgoing.bytes": _("Number of outgoing bytes "
                                    "on the network for a VM interface"),
        "network.incoming.packets": _("Number of incoming "
                                      "packets for a VM interface"),
        "network.outgoing.packets": _("Number of outgoing "
                                      "packets for a VM interface"),
        "network.incoming.bytes.rate": _("Average rate per sec of incoming "
                                         "bytes on a VM network interface"),
        "network.outgoing.bytes.rate": _("Average rate per sec of outgoing "
                                         "bytes on a VM network interface"),
        "network.incoming.packets.rate": _("Average rate per sec of incoming "
                                           "packets on a VM network interface"),
        "network.outgoing.packets.rate": _("Average rate per sec of outgoing "
                                           "packets on a VM network interface"),
        "network": _("Existence of network"),
        'network.create': _("Creation requests for this network"),
        'network.update': _("Update requests for this network"),
        'subnet': _("Existence of subnet"),
        'subnet.create': _("Creation requests for this subnet"),
        'subnet.update': _("Update requests for this subnet"),
        'port':  _("Existence of port"),
        'port.create': _("Creation requests for this port"),
        'port.update': _("Update requests for this port"),
        'router': _("Existence of router"),
        'router.create': _("Creation requests for this router"),
        'router.update': _("Update requests for this router"),
        'ip.floating': _("Existence of floating ip"),
        'ip.floating.create': _("Creation requests for this floating ip"),
        'ip.floating.update': _("Update requests for this floating ip"),
        'image': _("Image existence check"),
        'image.size': _("Uploaded image size"),
        'image.update': _("Number of image updates"),
        'image.upload': _("Number of image uploads"),
        'image.delete': _("Number of image deletions"),
        'image.download': _("Image is downloaded"),
        'image.serve': _("Image is served out"),
        'volume': _("Existence of volume"),
        'volume.size': _("Size of volume"),
        'storage.objects': _("Number of objects"),
        'storage.objects.size': _("Total size of stored objects"),
        'storage.objects.containers': _("Number of containers"),
        'storage.objects.incoming.bytes': _("Number of incoming bytes"),
        'storage.objects.outgoing.bytes': _("Number of outgoing bytes"),
        'storage.api.request': _("Number of API requests against swift"),
        'energy': _("Amount of energy"),
        'power': _("Power consumption"),
        'hardware.ipmi.node.power': _("System Current Power"),
        'hardware.ipmi.fan': _("Fan RPM"),
        'hardware.ipmi.temperature': _("Sensor Temperature Reading"),
        'hardware.ipmi.current': _("Sensor Current Reading"),
        'hardware.ipmi.voltage': _("Sensor Voltage Reading"),
        'hardware.ipmi.node.temperature': _("System Temperature Reading"),
        'hardware.ipmi.node.outlet_temperature': _("System Outlet Temperature Reading"),
        'hardware.ipmi.node.airflow': _("System Airflow Reading"),
        'hardware.ipmi.node.cups': _("System CUPS Reading"),
        'hardware.ipmi.node.cpu_util': _("System CPU Utility Reading"),
        'hardware.ipmi.node.mem_util': _("System Memory Utility Reading"),
        'hardware.ipmi.node.io_util': _("System IO Utility Reading")
    }

    def __init__(self, apiresource):
        super(Meter, self).__init__(apiresource)
        self._description = self._metrics_description.get(self._name, '')

    def augment(self, label=None, description=None):
        if label:
            self._label = label
        if description:
            self._description = description

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def resource_id(self):
        return self._resource_id

    @staticmethod
    def find_and_create(client, meter_id):
        return Meter(client.metric.get(meter_id))


class ResourceType(base.APIResourceWrapper):
    _attrs = ['name', 'state']

    def __init__(self, apiresource):
        super(ResourceType, self).__init__(apiresource)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @staticmethod
    list_resource_types(gnocchiclient):
        return gnocchi_client.resource_type.list()

    @staticmethod
    init_resource_types(gnocchiclient):
        resource_types = Resource.list_resource_types(gnocchi_client)
        return [ResourceType(res_type) for res_type in resource_types if str(res_type['state']) == 'active']
            
class Resource(base.APIResourceWrapper):
    _attrs = ['id', 'type', 'display_name', 'source', 'user_id', 'project_id']

    def __init__(self, apiresource, gnocchiclient):
        super(Resource, self).__init__(apiresource)

        self.meters = {}
        for meter_name, meter_id in apiresource['metrics'].items():
            self.meters[meter_name] = Meter.find_and_create(gnocchiclient, meter_id)

    @property
    def name(self):
        name = self.display_name
        display_name = self.metadata.get("display_name", None)
        return name or display_name or ""

    @property
    def id(self):
        return self._id

    @property
    def tenant(self):
        return self._tenant

    @property
    def user_id(self):
        return self._user_id

    @property
    def meters(self):
        return self.meters

    @staticmethod
    def get_resource(gnocchiclient, resource_type, resource_id):
        return gnocchi_client.resource.get(resource_type, resource_id)

    @staticmethod
    def list_resource(gnocchiclient, resource_type='generic'):
        return gnocchiclient.resource.list(resource_type)

    @staticmethod
    def init_resources(gnocchiclient, resource_type, project_id):
        # TODO(Bogdan): Should use search instead of list. Need to find out
        # how querying works for the gnocchi client
        resources = gnocchiclient.resource.list(resource_type)
        return [Resource(resource) for resource in resources if str(resource['project_id']) == project_id]
    
    def get_meter(self, meter_name):
        return self.meters.get(meter_name, '')

    def set_meter(self, meter_name, value):
        self._meters[meter_name] = value
