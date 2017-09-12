
from .....collections import (SchemaDict, RequiredSchemaDict)


class Capability(object):
    def __init__(self):
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.valid_source_types = []


class Root(Capability):
    pass


class Node(Root):
    pass


class Container(Root):
    def __init__(self):
        super(Container, self).__init__()

        self.properties.schema['num_cpus'] = int
        #self.properties.schema['cpu_frequency'] = scalar-unit.frequency
        #self.properties.schema['disk_size'] = scalar-unit.size
        #self.properties.schema['mem_size'] = scalar-unit.size


class OperatingSystem(Root):
    def __init__(self):
        super(OperatingSystem, self).__init__()

        self.properties.schema['architecture'] = str
        self.properties.schema['type'] = str
        self.properties.schema['distribution'] = str
        self.properties.schema['version'] = str


class Scalable(Root):
    def __init__(self):
        super(Scalable, self).__init__()

        self.properties.schema['min_instances'] = int
        self.properties['min_instances'] = 1
        self.properties.schema['max_instances'] = int
        self.properties['max_instances'] = 1
        self.properties.schema['default_instances'] = int


class Attachment(Root):
    pass


class Endpoint(Root):
    Admin = None

    def __init__(self):
        super(Endpoint, self).__init__()

        self.properties.schema['protocol'] = str
        self.properties['protocol'] = 'tcp'
        #self.properties.schema['port'] = osca.datatypes.network.PortDef
        self.properties.schema['secure'] = bool
        self.properties['secure'] = False
        self.properties.schema['url_path'] = str
        self.properties.schema['port_name'] = str
        self.properties.schema['network_name'] = str
        self.properties.schema['initiator'] = str
        self.properties.schema['ports'] = dict # of tosca.datatypes.network.PortSpec

        self.attributes.schema['ip_address'] = str


class EndpointAdmin(Endpoint):
    def __init__(self):
        super(EndpointAdmin, self).__init__()

        self.properties['secure'] = True


Endpoint.Admin = EndpointAdmin


import network
