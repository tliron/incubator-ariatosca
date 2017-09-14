#!/usr/bin/env python

from aria_extension_tosca.simple_v1_0_py.profile import tosca
from aria import myfuncs

# Node Templates

vm = tosca.nodes.BlockStorage

vm = tosca.nodes.Compute('vm')
vm.attributes['private_address'] = 'localhost'
vm.capabilities['os'].properties.update(
    architecture=myfuncs.get_architecture(),
    type=myfuncs.get_type(),
    distribution=myfuncs.get_distribution(),
    version=myfuncs.get_version()
)
vm.capabilities['host'].properties['num_cpus'] = 4
vm.interfaces['Standard'].operations['create'].implementation = 'scripts/vm/create.sh'

disk = tosca.nodes.BlockStorage('disk')
disk.properties['size'] = tosca.scalar_unit.size('10 GB')

nginx = tosca.nodes.WebServer('nginx')

nodecellar = tosca.nodes.WebApplication('nodecellar')
nodecellar.properties.update(
    component_version=tosca.version('1.2'),
    admin_credential=tosca.datatypes.Credential(dict(user='aria', token='aria123'))
)
nodecellar.capabilities['app_endpoint'].properties.update(
    protocol='http',
    port=tosca.datatypes.network.PortDef(8080),
    url_path='/nodecellar'
)

# Topology

topology = tosca.Topology('nodecellar')
topology.node_templates.extend((vm, disk, nginx, nodecellar))

vm.requirements['local_storage'].add(node_template='disk')
nginx.requirements['host'].add(node_template='vm')
nodecellar.requirements['host'].add(node_template='nginx')

topology.validate()
