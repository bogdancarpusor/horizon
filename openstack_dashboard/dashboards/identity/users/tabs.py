from horizon import tabs
from horizon import tables as horizon_tables
from horizon import exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from openstack_dashboard.dashboards.identity.users import tables
from openstack_dashboard.dashboards.identity.users.models import User
from openstack_dashboard.utils import identity
from openstack_dashboard import policy
from openstack_dashboard import api


class KeystoneUsersTab(tabs.TableTab, horizon_tables.DataTableView):
    table_classes = (tables.KeystoneUsersTable,)
    name = tables.KeystoneUsersTable.Meta.verbose_name
    slug = tables.KeystoneUsersTable.Meta.name
    template_name = 'horizon/common/_detail_table.html'

    def get_filters(self):
        self.table = self._tables['keystone_users']
        self.handle_server_filter(self.request, table=self.table)
        self.update_server_filter_action(self.request, table=self.table)

        return super(KeystoneUsersTab, self).get_filters()
    def needs_filter_first(self, table):
        return self._needs_filter_first


    def get_keystone_users_data(self):
        users = []
        filters = self.get_filters()
        self._needs_filter_first = False

        if policy.check(
            (("identity", "identity:list_users"),),self.request):

            # If filter_first is set and if there are not other filters
            # selected, then search criteria must be provided
            # and return an empty list

            filter_first = getattr(settings, 'FILTER_DATA_FIRST', {})
            if filter_first.get('identity.users', False) and len(filters) == 0:
                self._needs_filter_first = True
                return users

            domain_id = identity.get_domain_id_for_operation(self.request)
            try:
                users = api.keystone.user_list(self.request,
                                               domain=domain_id,
                                               filters=filters)
            except Exception:
                exceptions.handle(self.request,
                                  _('Unable to retrieve user list.'))
        elif policy.check((("identity", "identity:get_user"),),
                          self.request):
            try:
                user = api.keystone.user_get(self.request,
                                             self.request.user.id,
                                             admin=False)
                users.append(user)
            except Exception:
                exceptions.handle(self.request,
                                  _('Unable to retrieve user information.'))
        else:
            msg = _("Insufficient privilege level to view user information.")
            messages.info(self.request, msg)

        if api.keystone.VERSIONS.active >= 3:
            domain_lookup = api.keystone.domain_lookup(self.request)
            for u in users:
                u.domain_name = domain_lookup.get(u.domain_id)
        return users
 

class GarrUsersTab(tabs.TableTab):
    table_classes = (tables.GarrUsersTable,)
    name = tables.GarrUsersTable.Meta.verbose_name
    slug = tables.GarrUsersTable.Meta.name
    template_name = 'horizon/common/_detail_table.html'

    def get_garr_users_data(self):
        users = User.objects.all()
        return users


class UsersTabs(tabs.TabGroup):
    slug = "users"
    tabs = (KeystoneUsersTab, GarrUsersTab)
    sticky = True
