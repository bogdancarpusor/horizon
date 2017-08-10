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

from horizon import exceptions
from horizon import forms
from horizon import workflows

from keystoneauth1.identity.v3 import token
from gnocchi import gnocchi_client, Resource, ResourceType
import pdb

class SelectResourceTypeAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(SelectResourceTypeAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve resource types list. '
                    'Please try again later.')
        context = args[0]
        
        default_role_field_name = self.get_default_role_field_name()
        self.fields[default_role_field_name] = forms.CharField(required=False)
        self.fields[default_role_field_name].initial = 'member'
        field_name = self.get_member_field_name('member')
        self.fields[field_name] = forms.MultipleChoiceField(required=False)
        try:
            client = gnocchi_client(request)
            resource_types = ResourceType.init_resource_types(client)
            self.fields[field_name].choices = [(resource_type.name, resource_type.name) 
                                               for resource_type in resource_types]
            resource_types = request.session['gnocchi'].get('resource_types', [])
            self.fields[field_name].initial = resource_types
        except Exception:
            exceptions.handle(self.request,
                                  _('Unable to retrieve resource type information.'))
    class Meta(object):
        name = _("Resource Type")
        slug = "select_resource_type"


class SelectResourceTypeStep(workflows.UpdateMembersStep):
    action_class = SelectResourceTypeAction
    help_text = _("Select the projects where the flavors will be used. If no "
                  "projects are selected, then the flavor will be available "
                  "in all projects.")
    available_list_title = _("All Projects")
    members_list_title = _("Selected Resource Types")
    no_available_text = _("No resource types found.")
    no_members_text = _("No resource types selected. ")
    show_roles = False
    contributes = ("resource_type")
    def contribute(self, data, context):
        if data:
            member_field_name = self.get_member_field_name('member')
            context['resource_type'] = data.get(member_field_name, [])
        return context

class SelectResourceType(workflows.Workflow):
    slug = "select_resource_type"
    name = _("Select Resource Type")
    finalize_button_name = _("Select")
    success_message = _('Selected resource types "%s".')
    failure_message = _('Unable to select resource types "%s".')
    success_url = "horizon:admin:metrics:index"
    default_steps = (SelectResourceTypeStep,)

    def format_status_message(self, message):
        return message % ', '.join(self.context['resource_type'])

    def handle(self, request, data):
        try:
            self.request.session['gnocchi']['resource_types'] = data['resource_type']
            self.request.session.modified = True
            return True
        except Exception:
            return False

class SelectResourceAction(workflows.MembershipAction):
    def __init__(self, request, *args, **kwargs):
        super(SelectResourceAction, self).__init__(request,
                                                       *args,
                                                       **kwargs)
        err_msg = _('Unable to retrieve resources list. '
                    'Please try again later.')
        context = args[0]
        
        default_role_field_name = self.get_default_role_field_name()
        self.fields[default_role_field_name] = forms.CharField(required=False)
        self.fields[default_role_field_name].initial = 'member'

        field_name = self.get_member_field_name('member')
        self.fields[field_name] = forms.MultipleChoiceField(required=False)
        try:
            client = gnocchi_client(request)
            project_id = request.user.project_id
            
            resource_types = request.session['gnocchi'].get('resource_types', [])
            if not resource_types: return []
            resource_types = [resource_type for resource_type in resource_types]
            resources = Resource.init_resources(client, resource_types, project_id)
            self.fields[field_name].choices = [("%s?=%s" % (resource.id, resource.type), resource.name) 
                                               for  resource in resources]
            
            resources = request.session['gnocchi'].get('resources', [])
            self.fields[field_name].initial = resources
        except Exception:
            exceptions.handle(self.request,
                                  _('Unable to retrieve resources information.'))
    
    class Meta(object):
        name = _("Resources")
        slug = "select_resources"

class SelectResourceStep(workflows.UpdateMembersStep):
    action_class = SelectResourceAction
    help_text = _("Select the resources for which metrics will be listed.")
    available_list_title = _("All Resources")
    members_list_title = _("Selected Resources")
    no_available_text = _("No resources found.")
    no_members_text = _("No resources selected. ")
    show_roles = False
    contributes = ("resource")

    def contribute(self, data, context):
        if data:
            member_field_name = self.get_member_field_name('member')
            context['resource'] = data.get(member_field_name, [])
        return context
    
class SelectResource(workflows.Workflow):
    slug = "select_resource"
    name = _("Select Resource")
    finalize_button_name = _("Select")
    success_message = _('Selected resources "%s".')
    failure_message = _('Unable to select resource "%s".')
    success_url = "horizon:admin:metrics:index"
    default_steps = (SelectResourceStep,)

    def format_status_message(self, message):
        return message % ', '.join(self.context['resource'])

    def handle(self, request, data):
        try:
            self.request.session['gnocchi']['resources'] = data['resource']
            self.request.session.modified = True
            return True
        except Exception:
            return False
