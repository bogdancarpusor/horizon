# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
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

import collections
import logging

from django.conf import settings
from django.forms import ValidationError
from django import forms as django_forms
from django import http
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables

from horizon import exceptions
from horizon import forms
from horizon import messages
from horizon.utils import functions as utils
from horizon.utils import validators

from openstack_dashboard import api
from workflow import gnocchi_client, ResourceType
LOG = logging.getLogger(__name__)
import pdb

class SelectResourceTypeForm(forms.SelfHandlingForm):
    resource_type = forms.CharField(label=_("Resource Type"),
                                      required=True,
                                      widget=forms.widgets.CheckboxInput)
    
    def __init__(self, *args, **kwargs):
        super(SelectResourceTypeForm, self).__init__(*args, **kwargs)

        try:
            resource_types = ResourceType.init_resource_types(gnocchi_client(self.request))
        except Exception:
            redirect = reverse("horizon:admin:metrics:index")
            exceptions.handle(self.request,
                              _("Unable to retrieve resource types."),
                              redirect=redirect)

        
        #self.fields['resource_type'].choices = [resource_type.name for resource_type in resource_types]
        self.fields['resource_type'].choices = [('a', 0), ('b', 1), ('c', 2)]

    def handle(self, request, data):
        pass