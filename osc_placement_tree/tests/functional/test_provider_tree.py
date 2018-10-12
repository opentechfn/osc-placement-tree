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
import subprocess

from osc_placement_tree.tests.functional import base
from osc_placement_tree.tests import uuids


class TestProviderTree(base.TestBase):

    def setUp(self):
        super(TestProviderTree, self).setUp()

        self.create_rp('compute0_with_disk')
        self.set_traits('compute0_with_disk',
                        ['HW_CPU_X86_SSE2',
                         'HW_CPU_X86_SSE',
                         'HW_CPU_X86_MMX'])
        self.create_rp('compute0_with_disk_NUMA0',
                       parent_rp_name='compute0_with_disk')
        self.create_rp('compute0_with_disk_NUMA1',
                       parent_rp_name='compute0_with_disk')

        self.update_inventory('compute0_with_disk',
                              'DISK_GB=256',
                              'DISK_GB:reserved=16')

        self.update_inventory('compute0_with_disk_NUMA0',
                              'VCPU=4',
                              'VCPU:allocation_ratio=16.0',
                              'VCPU:reserved=1',
                              'MEMORY_MB=16384',
                              'MEMORY_MB:reserved=1024')

        self.update_inventory('compute0_with_disk_NUMA1',
                              'VCPU=4',
                              'VCPU:allocation_ratio=16.0',
                              'MEMORY_MB=16384')

        self.create_rp('compute1_with_disk')
        self.set_traits('compute1_with_disk',
                        ['HW_CPU_X86_MMX'])
        self.create_rp('compute1_with_disk_NUMA0',
                       parent_rp_name='compute1_with_disk')
        self.create_rp('compute1_with_disk_NUMA1',
                       parent_rp_name='compute1_with_disk')

        self.update_inventory('compute1_with_disk',
                              'DISK_GB=128',
                              'DISK_GB:reserved=16')

        self.update_inventory('compute1_with_disk_NUMA0',
                              'VCPU=8',
                              'VCPU:allocation_ratio=16.0',
                              'VCPU:reserved=1',
                              'MEMORY_MB=16384',
                              'MEMORY_MB:reserved=1024')

        self.update_inventory('compute1_with_disk_NUMA1',
                              'VCPU=8',
                              'VCPU:allocation_ratio=16.0',
                              'MEMORY_MB=16384')

        self.set_aggregate('compute0_with_disk',
                           [uuids.host_aggregate1, uuids.agg2])
        self.set_aggregate('compute1_with_disk',
                           [uuids.host_aggregate1, uuids.agg2])

        self.set_aggregate('compute0_with_disk_NUMA0', [uuids.agg2])
        self.set_aggregate('compute0_with_disk_NUMA1', [uuids.agg2])
        self.set_aggregate('compute1_with_disk_NUMA0', [uuids.agg2])
        self.set_aggregate('compute1_with_disk_NUMA1', [uuids.agg2])

    def test_provider_tree_show(self):
        dot_src = self.openstack('resource provider tree show %s' %
                                 uuids.compute0_with_disk)
        self.assertDot(dot_src)

    def test_provider_tree_show_with_fields(self):
        dot_src = self.openstack('resource provider tree show %s '
                                 '--fields uuid,name,generation'
                                 % uuids.compute0_with_disk)
        self.assertDot(dot_src)

    def test_provider_tree_show_not_existing_uuid(self):
        ex = self.assertRaises(
            subprocess.CalledProcessError,
            self.openstack,
            'resource provider tree show %s' % uuids.not_existing_rp)
        self.assertIn('does not exists', ex.output)

    def test_provider_tree_list(self):
        dot_src = self.openstack('resource provider tree list')
        self.assertDot(dot_src)

    def test_provider_tree_list_with_fields(self):
        dot_src = self.openstack('resource provider tree list '
                                 '--fields uuid,name,generation')
        self.assertDot(dot_src)
