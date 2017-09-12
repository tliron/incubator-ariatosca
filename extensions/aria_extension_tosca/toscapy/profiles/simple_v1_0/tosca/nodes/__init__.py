
from .. import Template
from .....collections import (SchemaDict, RequiredSchemaDict)
from platform import node


class NodeTemplate(Template):
    def __init__(self, name=None):
        super(NodeTemplate, self).__init__(name)
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.interfaces = {}
        self.capabilities = {}
        self.requirements = {}


class Requirement(object):
    def __init__(self, capability=None, node=None, relationship=None):
        self.capability = capability
        self.node = node
        self.relationship = relationship
        self.assignments = []

    def add(self, node_template=None):
        self.assignments.append(dict(node_template=node_template))


class Root(NodeTemplate):
    def __init__(self, name=None):
        super(Root, self).__init__(name)
        from ... import tosca

        self.attributes.schema['tosca_id'] = str
        self.attributes.schema['tosca_name'] = str
        self.attributes.schema['state'] = str
        self.attributes['state'] = 'initial'

        self.interfaces['Standard'] = tosca.interfaces.node.lifecycle.Standard()

        self.capabilities['feature'] = tosca.capabilities.Node()

        self.requirements['dependency'] = Requirement(
            capability=tosca.capabilities.Node,
            node=tosca.nodes.Root,
            relationship=tosca.relationships.DependsOn
        )


class Compute(Root):
    def __init__(self, name=None):
        super(Compute, self).__init__(name)
        from ... import tosca

        self.attributes.schema['private_address'] = str
        self.attributes.schema['public_address'] = str
        self.attributes.schema['networks'] = dict # of tosca.datatypes.network.NetworkInfo
        self.attributes.schema['ports'] = dict # of tosca.datatypes.network.PortInfo

        self.capabilities['host'] = tosca.capabilities.Container()
        self.capabilities['host'].valid_source_types.append(tosca.nodes.SoftwareComponent)
        self.capabilities['binding'] = tosca.capabilities.network.Bindable()
        self.capabilities['os'] = tosca.capabilities.OperatingSystem()
        self.capabilities['scalable'] = tosca.capabilities.Scalable()

        self.requirements['local_storage'] = Requirement(
            capability=tosca.capabilities.Attachment,
            node=tosca.nodes.BlockStorage,
            relationship=tosca.relationships.AttachesTo
        )


class BlockStorage(Root):
    def __init__(self, name=None):
        super(BlockStorage, self).__init__(name)
        from ... import tosca

        self.properties.schema['size'] = int # scalar-unit.size
        self.properties.schema['volume_id'] = str
        self.properties.schema['snapshot_id'] = str

        self.capabilities['attachment'] = tosca.capabilities.Attachment()


class SoftwareComponent(Root):
    def __init__(self, name=None):
        super(SoftwareComponent, self).__init__(name)
        from ... import tosca

        #self.properties.schema['component_version'] = version
        #self.properties.schema['admin_credential'] = tosca.datatypes.Credential

        self.requirements['host'] = Requirement(
            capability=tosca.capabilities.Container,
            node=tosca.nodes.Compute,
            relationship=tosca.relationships.HostedOn
        )


class WebServer(SoftwareComponent):
    def __init__(self, name=None):
        super(WebServer, self).__init__(name)
        from ... import tosca

        self.capabilities['data_endpoint'] = tosca.capabilities.Endpoint()
        self.capabilities['admin_endpoint'] = tosca.capabilities.Endpoint.Admin()
        self.capabilities['host'] = tosca.capabilities.Container()
        self.capabilities['host'].valid_source_types.append(tosca.nodes.WebApplication)


class WebApplication(SoftwareComponent):
    def __init__(self, name=None):
        super(WebApplication, self).__init__(name)
        from ... import tosca

        self.properties.schema['context_root'] = str

        self.capabilities['app_endpoint'] = tosca.capabilities.Endpoint()

        self.requirements['host'] = Requirement(
            capability=tosca.capabilities.Container,
            node=tosca.nodes.WebServer,
            relationship=tosca.relationships.HostedOn
        )
