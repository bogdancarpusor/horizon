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
from workflow import gnocchi_client, ResourceType, Resource, Meter
from openstack_dashboard.dashboards.admin.metrics import \
    tables as metrics_tables
import pdb

RESOURCES = [
{u'created_by_project_id': 'd4ff53f5c48f4d8f88dfc07539bd8315',
 u'created_by_user_id': u'43f30fdec97d4996a17d720f6e00310e',
 u'creator': u'43f30fdec97d4996a17d720f6e00310e:d4ff53f5c48f4d8f88dfc07539bd8315',
 u'display_name': u'testcb-eph',
 u'ended_at': None,
 u'flavor_id': u'1',
 u'flavor_name': u'm1.tiny',
 u'host': u'ba1-r2-s06',
 u'id': u'06e76595-4155-4bbc-a7ec-8ea99117f019',
 u'image_ref': u'fb8a49b9-4e83-40e0-8cda-3a28d75c16cb',
 u'metrics': {u'compute.instance.booting.time': u'b7498998-155b-4ad9-94e5-00fa3179e836',
              u'cpu': u'cc713905-d97e-4497-999e-744072844a8a',
              u'cpu.delta': u'6df5d2a4-34b2-4d16-9e1b-46df79080950',
              u'cpu_l3_cache': u'7d84401f-39e2-49e4-94ad-64598b1b8763',
              u'cpu_util': u'545e3af3-8a3e-4254-860e-f9c48894c759',
              u'disk.allocation': u'5eec9723-0ee0-47dc-9fc5-5fa368fc21bf',
              u'disk.capacity': u'6fe2bd29-58bc-4a51-b2e8-1bf5a93a016e',
              u'disk.ephemeral.size': u'693d4fd5-486e-4880-bdb8-fc43ad7650bc',
              u'disk.iops': u'fa89a314-d0be-45cd-a28e-f441cda180b2',
              u'disk.latency': u'fb2721d5-b02c-45d3-8b47-63dfb76ef945',
              u'disk.read.bytes': u'40a4a9f0-ee60-4ea2-9f25-c60edde2be2e',
              u'disk.read.bytes.rate': u'ddee502d-8d97-4088-924c-9b2cab7cb96c',
              u'disk.read.requests': u'05b6301d-103b-4d65-8c7d-a5abbfdbfbd4',
              u'disk.read.requests.rate': u'5eefa518-e06e-4fe1-85f7-894c71dc4620',
              u'disk.root.size': u'7cd83e0e-c0a8-4dd6-b94c-2b8f54bc2e19',
              u'disk.usage': u'48f1509e-15f3-44f1-9600-988084f4b5a8',
              u'disk.write.bytes': u'86bf4363-35d1-45e5-aaee-1ca38350cbfc',
              u'disk.write.bytes.rate': u'944048f0-667e-46c4-a876-93e5a0af0c0c',
              u'disk.write.requests': u'b46b17cb-2f93-4300-b212-736f4afaf9b3',
              u'disk.write.requests.rate': u'6ab46a41-671c-4f25-9ccf-ff3acc777b94',
              u'memory': u'dc262cbe-7772-4961-9b3a-166bdb7fe283',
              u'memory.bandwidth.local': u'72d46e38-cd80-4710-8544-16dea242b65c',
              u'memory.bandwidth.total': u'55916dee-0037-4604-9ff1-008746fc53c0',
              u'memory.resident': u'22dc9c81-7d40-4e4a-a0a4-9d65f03af84c',
              u'memory.usage': u'bcf1d1a2-c13e-4fd5-8df3-032c987a5d8f',
              u'perf.cache.misses': u'c1470b15-3ab4-4362-9c93-17e2baa3611e',
              u'perf.cache.references': u'4cee8695-f93b-4d83-954c-d06088201347',
              u'perf.cpu.cycles': u'45bfb471-4f3c-4667-bf38-6c01af864202',
              u'perf.instructions': u'd0e36ac4-1d57-45d1-b476-18a6754adb92',
              u'vcpus': u'88d03a18-247c-446b-b921-1dd724bbc22b'},
 u'original_resource_id': u'06e76595-4155-4bbc-a7ec-8ea99117f019',
 u'project_id': u'9257947f992b4d17bdbbe082569b9ccc',
 u'revision_end': None,
 u'revision_start': u'2017-07-13T09:16:35.791133+00:00',
 u'server_group': None,
 u'started_at': u'2017-07-13T09:16:35.791112+00:00',
 u'type': u'instance',
 u'user_id': u'cc0530ce0f98408c9732ab346dd05872'},
{u'created_by_project_id': u'd4ff53f5c48f4d8f88dfc07539bd8315',
 u'created_by_user_id': u'43f30fdec97d4996a17d720f6e00310e',
 u'creator': u'43f30fdec97d4996a17d720f6e00310e:d4ff53f5c48f4d8f88dfc07539bd8315',
 u'display_name': u'testcb',
 u'ended_at': None,
 u'flavor_id': u'1',
 u'flavor_name': u'm1.tiny',
 u'host': u'ba1-r2-s06',
 u'id': u'2e33d61a-b975-4768-b478-8da64de05f6c',
 u'image_ref': None,
 u'metrics': {u'compute.instance.booting.time': u'26361c0b-d5d9-4083-986c-c786f52bdb7b',
              u'cpu': u'4d9c7197-447d-492f-8c47-4d90fa9fc68a',
              u'cpu.delta': u'ff4df8bc-2021-4731-a660-7b87e966f680',
              u'cpu_l3_cache': u'9f327f83-b18a-4783-bb2a-588b76bfd55b',
              u'cpu_util': u'f5d672fa-be17-4e22-88c4-69ad9e4fb13f',
              u'disk.allocation': u'0e751bdf-0b25-4ce1-a41e-04164c826eb0',
              u'disk.capacity': u'4c2ceb0d-48c8-4da7-b65b-ad3dc5932ac1',
              u'disk.ephemeral.size': u'af18064f-e7a0-4842-85eb-63e8addb6a35',
              u'disk.iops': u'ca4720f9-0706-497b-b158-92d39eaee465',
              u'disk.latency': u'd32ca74b-03f1-4c24-8147-ddeab68ecd87',
              u'disk.read.bytes': u'ce923c11-e655-4044-af51-6085c6486f71',
              u'disk.read.bytes.rate': u'f604b620-52cd-47bc-a0c3-56fb31468fd7',
              u'disk.read.requests': u'3ebc2afc-62b5-4413-acd4-276aa2fe474a',
              u'disk.read.requests.rate': u'2b80ca00-916d-440e-9845-82b7fb7bf480',
              u'disk.root.size': u'f6d9e78d-bad1-42fc-ba00-85206a2eb760',
              u'disk.usage': u'c44eef7a-cb8b-45fc-8f39-005209a7b51c',
              u'disk.write.bytes': u'b2ee311b-0a35-4c5c-8d73-9b97a7621741',
              u'disk.write.bytes.rate': u'147dfe73-4e7a-42e8-ab3f-ca3150900271',
              u'disk.write.requests': u'260e78f1-c817-48b4-9117-fb74611bd631',
              u'disk.write.requests.rate': u'4457a63a-35eb-493b-95ee-6068cd9d55ee',
              u'memory': u'e974f792-b626-450e-b324-27d4d642a3f9',
              u'memory.bandwidth.local': u'd9560f07-81cd-4746-843b-271c31065980',
              u'memory.bandwidth.total': u'72f520da-876f-4e41-a4da-99a55d7df6ec',
              u'memory.resident': u'54257964-c0b8-4182-9e15-bdba34aff8b1',
              u'memory.usage': u'6ea244e8-fcd4-4c35-a932-a0ab6a109742',
              u'perf.cache.misses': u'158ee422-f1bd-4b3d-8cc5-e8bb4b966e3a',
              u'perf.cache.references': u'2c9824a8-0960-4578-8a17-3d84f156fe75',
              u'perf.cpu.cycles': u'bfd58068-7802-4955-aed7-e834ea9f2e80',
              u'perf.instructions': u'8534d868-f2c3-43cb-ab93-1f429fe459f8',
              u'vcpus': u'cfacbc83-0406-459e-a2c9-0e5cb055a9e6'},
 u'original_resource_id': u'2e33d61a-b975-4768-b478-8da64de05f6c',
 u'project_id': u'9257947f992b4d17bdbbe082569b9ccc',
 u'revision_end': None,
 u'revision_start': u'2017-07-13T09:16:39.050122+00:00',
 u'server_group': None,
 u'started_at': u'2017-07-13T09:16:39.050096+00:00',
 u'type': u'instance',
 u'user_id': u'cc0530ce0f98408c9732ab346dd05872'},
{u'created_by_project_id': u'd4ff53f5c48f4d8f88dfc07539bd8315',
 u'created_by_user_id': u'43f30fdec97d4996a17d720f6e00310e',
 u'creator': u'43f30fdec97d4996a17d720f6e00310e:d4ff53f5c48f4d8f88dfc07539bd8315',
 u'display_name': u'test',
 u'ended_at': None,
 u'flavor_id': u'3',
 u'flavor_name': u'm1.medium',
 u'host': u'ba1-r2-s06',
 u'id': u'dcaf2c23-1da7-4ca0-853c-541574323aed',
 u'image_ref': u'fb8a49b9-4e83-40e0-8cda-3a28d75c16cb',
 u'metrics': {u'compute.instance.booting.time': u'9ac1f109-d04b-4a22-adf0-096565ae810f',
              u'cpu': u'2931bc55-35cb-4e27-bdf5-31fc405a1b0d',
              u'cpu.delta': u'70b1a8bb-141e-4496-9211-a124800314e8',
              u'cpu_l3_cache': u'b58a5218-9cea-47e5-8f34-cc80f6ca14d3',
              u'cpu_util': u'0cd6c6dc-4ab5-4fbf-a90b-5e2157f4efd3',
              u'disk.allocation': u'f9be9662-57e1-4cf1-9121-72203cfd0899',
              u'disk.capacity': u'db13aa3d-0458-4fa6-a8e1-65f24484c721',
              u'disk.ephemeral.size': u'3dc3e46a-2247-48bf-8517-ed8e16c1a999',
              u'disk.iops': u'72a13a09-5384-41e6-953a-262401211d8e',
              u'disk.latency': u'07505072-d751-47ef-9e91-239c9e7017f0',
              u'disk.read.bytes': u'30feb139-40cb-4783-9b2b-b9d57b2a2dda',
              u'disk.read.bytes.rate': u'3a3334fc-8b60-497b-abca-044a7d0c3c0a',
              u'disk.read.requests': u'25ec1d3f-b922-4273-932c-35de1500c7fc',
              u'disk.read.requests.rate': u'af710a16-2086-4851-b3a1-a7e434897aa6',
              u'disk.root.size': u'3ddb15a1-7ce3-4694-9580-6a680a7dd545',
              u'disk.usage': u'f4495fb6-76b0-478b-ae2c-2414184594f7',
              u'disk.write.bytes': u'c60a3e17-b620-4324-8c1d-25be48a0d4cc',
              u'disk.write.bytes.rate': u'a7b784b6-1db2-4486-aa3f-343e4a6eea82',
              u'disk.write.requests': u'61a5a9d5-26b1-40b2-840f-96533f428177',
              u'disk.write.requests.rate': u'3730836e-5507-4ab9-873a-fe0499789b3f',
              u'memory': u'b5d6dd2e-8ad8-4345-9f7a-ad9929480b0d',
              u'memory.bandwidth.local': u'fb75b99a-bcea-47a8-afa5-640cbefc6b6b',
              u'memory.bandwidth.total': u'0c6ad5fc-c00a-450b-be55-56c2aaeb1a6f',
              u'memory.resident': u'aae1c904-b9f2-47fe-b693-c9c5511b096c',
              u'memory.usage': u'f0cece31-3743-4de7-a544-f7b95a72bbb2',
              u'perf.cache.misses': u'15c605d0-fc20-4813-8ad9-596c350203b2',
              u'perf.cache.references': u'd589a639-3025-42ce-b917-8390c88efb1f',
              u'perf.cpu.cycles': u'42079fc4-7de1-48c5-90f3-3f5673d47d70',
              u'perf.instructions': u'00f4ed8d-b3ef-4fae-89de-78605a95bd37',
              u'vcpus': u'83acc52b-d391-431a-a5df-b5b754ae1862'},
 u'original_resource_id': u'dcaf2c23-1da7-4ca0-853c-541574323aed',
 u'project_id': u'6e2eb2f22518495db3655c5bc1d2bd2c',
 u'revision_end': None,
 u'revision_start': u'2017-07-14T13:27:26.116156+00:00',
 u'server_group': None,
 u'started_at': u'2017-07-14T13:27:26.116099+00:00',
 u'type': u'instance',
 u'user_id': u'72a0254c67754b23b43ab0aae6524b50'},
{u'created_by_project_id': u'd4ff53f5c48f4d8f88dfc07539bd8315',
 u'created_by_user_id': u'43f30fdec97d4996a17d720f6e00310e',
 u'creator': u'43f30fdec97d4996a17d720f6e00310e:d4ff53f5c48f4d8f88dfc07539bd8315',
 u'display_name': u'newton',
 u'ended_at': None,
 u'flavor_id': u'1',
 u'flavor_name': u'm1.tiny',
 u'host': u'ba1-r2-s06',
 u'id': u'7f15c32d-0ddd-4f08-aea3-7d5a376899bc',
 u'image_ref': None,
 u'metrics': {u'compute.instance.booting.time': u'b1671100-4de4-4eb8-b688-48f8af3bf57d',
              u'cpu': u'ff01fcf7-f65e-4c2d-bd8f-8e0e5f882130',
              u'cpu.delta': u'8cc64c8a-3e06-44dc-b6f8-47147e2d8142',
              u'cpu_l3_cache': u'd405b5c6-cbbf-415f-9761-4e797aca47e5',
              u'cpu_util': u'b0c4209b-a25e-4726-9f84-86cb424b6f27',
              u'disk.allocation': u'79220be5-debe-4397-8c01-64d03f2f5afb',
              u'disk.capacity': u'a93dcf01-dd0e-4d91-87ec-18f6cf492310',
              u'disk.ephemeral.size': u'bcdf7b72-8391-4913-a5d6-094cb1b64d74',
              u'disk.iops': u'111ed1fd-8d9a-4fdb-8501-9a5abe4a02da',
              u'disk.latency': u'842ebeb3-ca10-42dd-a0c8-2589cb400402',
              u'disk.read.bytes': u'beb987c3-8136-4a83-9275-58239f14cdbd',
              u'disk.read.bytes.rate': u'2754421b-cfb1-419f-b9b4-7a17ea04d20e',
              u'disk.read.requests': u'a9fb08df-f797-4d04-8f78-04defacc707b',
              u'disk.read.requests.rate': u'55fa4e34-53fb-4caa-b9cd-077a930c1989',
              u'disk.root.size': u'ee86660b-53b7-4be7-9767-fb605baa4b49',
              u'disk.usage': u'c94dc289-0795-4904-950e-3c2b91307875',
              u'disk.write.bytes': u'340f07de-a754-4f61-9b80-82fb9e0ba3c0',
              u'disk.write.bytes.rate': u'794c7d9f-553d-419f-aa8f-a2ce53ea23b5',
              u'disk.write.requests': u'39f6d933-c940-40f9-ab44-39817b05256e',
              u'disk.write.requests.rate': u'57cd3c2a-fdbf-43fb-85ca-f286fe883b3e',
              u'memory': u'1339acf5-dabb-45dd-89d1-88ce0b9c145f',
              u'memory.bandwidth.local': u'c5052107-f6d9-437f-961b-1ae8ae7a1b7c',
              u'memory.bandwidth.total': u'471083bd-5fcc-4464-bd04-3cc69f9db365',
              u'memory.resident': u'216e4619-37fe-4e46-a70a-834024e20ade',
              u'memory.usage': u'd8ff7f27-33e8-4cad-beee-29857b3b889a',
              u'perf.cache.misses': u'be94c673-96cb-4266-8733-82331afdc332',
              u'perf.cache.references': u'744ccf1a-5887-4437-806e-634f702bb1c3',
              u'perf.cpu.cycles': u'9dd99ed1-009b-4683-93b5-9dfd6d82dec0',
              u'perf.instructions': u'0725310c-5320-4967-ad74-59c9d4e79238',
              u'vcpus': u'bb9018fb-a155-4a75-8bc7-1602a35fa7be'},
 u'original_resource_id': u'7f15c32d-0ddd-4f08-aea3-7d5a376899bc',
 u'project_id': u'9257947f992b4d17bdbbe082569b9ccc',
 u'revision_end': None,
 u'revision_start': u'2017-07-28T18:13:33.799372+00:00',
 u'server_group': None,
 u'started_at': u'2017-07-28T18:13:33.799338+00:00',
 u'type': u'instance',
 u'user_id': u'cc0530ce0f98408c9732ab346dd05872'}
]


class StatsTab(tabs.TableTab):
    name = _("Metrics")
    slug = "stats"
    template_name = "horizon/common/_detail_table.html"
    table_classes = (metrics_tables.UsageTable,)

    def get_usage_table_data(self):
        metrics = []
        try:
            client = gnocchi_client(self.request)
            resource_types = ResourceType.init_resource_types(client)
            resource_type_select = self._tables['usage_table'].base_actions['select_resource_type']
            resource_type_select.values = [resource_type.name for resource_type in resource_types]
            resource_type_select.initial_value = resource_types[0].name
            resource_type_select.values.append('another')
            
            resource_select = self._tables['usage_table'].base_actions['select_resource']
            resources = Resource.init_resources(client, resource_types[0].name, self.request.user.project_id)
            
            if len(resources) > 0:
                # Change to select metrics from a list of resources
                resource_select.values = [resource.name for resource in resources]
                resource_select.initial_value = resources[0].name
                for resource in resources:
                    if resource.name == resource_select.initial_value:
                        metrics.append(resource.get_metrics_dict)
        except KeyError:
            pass

        if len(metrics) == 0:
            resource = RESOURCES[0]
            for metric_name, metric_id in resource['metrics'].items():
                metrics.append({
                    'id': metric_id,
                    'meter': metric_name,
                    'resource': resource['display_name'],
                    'project': resource['project_id'],
                    'description': Meter._metrics_description.get(metric_name, ''),
                    'unit': ''
                })

        pdb.set_trace()    
        return metrics
        # [{
        #     'id': '0',
        #     'resource': 'resource1',
        #     'project': 'project1',
        #     'meter': 'meter2',
        #     'description': 'desc',
        #     'time': '01-01-2017',
        #     'value': '12',
        #     'unit': 'km'
        # }]

class MetricsValuesTab(tabs.TableTab):
    name = _("Metrics Values")
    slug = "metrics"
    template_name = "horizon/common/_detail_table.html"
    table_classes = (metrics_tables.ValuesTable,)

    def get_values_table_data(self):
        return []

class MetricsTabs(tabs.TabGroup):
    slug = "metrics"
    tabs = (StatsTab, MetricsValuesTab, )
    sticky = True
