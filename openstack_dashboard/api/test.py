from gnocchiclient import auth
from gnocchiclient.v1 import client

class GnocchiTokenNoAuthPlugin(auth.GnocchiNoAuthPlugin):
    """No authentication plugin that makes use of the user token
    """

    def __init__(self, user_id, token_id, project_id, roles, endpoint):
        super(GnocchiTokenNoAuthPlugin, self).__init__(user_id, project_id,
                                                       roles, endpoint)
        self._token = token_id

    def get_headers(self, session, **kwargs):
        return { 'x-user-id': self._user_id,
                 'x-auth-token': self._token,
                 'x-project-id': self._project_id,
                 #'x-roles': self._roles
                }

    def get_token(self, session, **kwargs):
        return self._token

user_id = '4d1b714eed534896802648996ae43843'
token_id = 'gAAAAABZeuj7FHxzM2C6OBXXy8B14gdop9aguCTAfQ6FQ9lV21qKM1-MrDIra2EEJMJ_myeuDM9du5fWQ10-W5za0aaZAXtDVqpuTs726kSph3wmYSHNI3I2XnQZ_fS5l2LWhX-cUO39GaTvR6nQMrr2K-0Wruls0G2bb052UoJUT4Wi8QofLa7j2FBxvd2_gLX4qL_Ah_HF'
project_id = '20c287b22a73483d8da82820c8dcdd9d'
roles = [{'name': u'admin'}]
endpoint = 'http://192.168.56.134:8041'
auth_plugin = GnocchiTokenNoAuthPlugin(user_id, token_id, project_id, roles, endpoint)
gnocchi = client.Client(session_options={'auth': auth_plugin})
print(gnocchi.resource.list('generic'))
