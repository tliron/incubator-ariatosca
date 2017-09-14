
from aria.modeling import models

from .. import Template
from .... import get_type_name
from ....collections import (SchemaDict, RequiredSchemaDict)
from platform import node


class NodeTemplate(Template):
    def __init__(self, name=None):
        super(NodeTemplate, self).__init__(name)
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.interfaces = {}
        self.capabilities = {}
        self.requirements = {}

    def validate(self):
        self.properties.validate()
        for interface in self.interfaces.itervalues():
            interface.validate()
        for capability in self.capabilities.itervalues():
            capability.validate()
        for requirement in self.requirements.itervalues():
            requirement.validate()

    def create_model(self, service_template):
        node_type = service_template.node_types.get_descendant(get_type_name(self.__class__))
        model = models.NodeTemplate(name=self.name, type=node_type)
        for prop in self.properties.create_models(models.Property):
            model.properties[prop.name] = prop
        for attribute in self.attributes.create_models(models.Attribute):
            model.attributes[attribute.name] = attribute
        for name, capability in self.capabilities.iteritems():
            capability = capability.create_model(service_template)
            capability.name = name
            model.capability_templates[name] = capability
        return model

    def fix_model(self, service_template):
        model = service_template.node_templates.get(self.name)
        for name, requirement in self.requirements.iteritems():
            for requirement in requirement.create_models(service_template):
                requirement.name = name
                model.requirement_templates.append(requirement)


class Requirement(object):
    def __init__(self, capability=None, node=None, relationship=None):
        self.capability = capability
        self.node = node
        self.relationship = relationship
        self.assignments = []

    def add(self, node_template=None):
        self.assignments.append(dict(node_template=node_template))

    def validate(self):
        pass

    def create_models(self, service_template):
        the_models = []
        for assignment in self.assignments:
            capability_type = \
                service_template.capability_types \
                .get_descendant(get_type_name(self.capability))
            node_template = assignment.get('node_template')
            if node_template is not None:
                node_template = service_template.node_templates.get(node_template)
                model = models.RequirementTemplate(target_capability_type=capability_type,
                                                   target_node_template=node_template)
                the_models.append(model)
        return the_models
        

class Root(NodeTemplate):
    def __init__(self, name=None):
        super(Root, self).__init__(name)
        from ... import tosca

        self.attributes.schema.update(
            tosca_id=str,
            tosca_name=str,
            state=str
        )
        self.attributes['state'] = 'initial'

        self.interfaces['Standard'] = tosca.interfaces.node.lifecycle.Standard()

        self.capabilities['feature'] = tosca.capabilities.Node()

        self.requirements['dependency'] = Requirement(
            capability=tosca.capabilities.Node,
            node=tosca.nodes.Root,
            relationship=tosca.relationships.DependsOn
        )


class Compute(Root):
    ROLE = 'host'
    
    def __init__(self, name=None):
        super(Compute, self).__init__(name)
        from ... import tosca

        self.attributes.schema.update(
            private_address=str,
            public_address=str,
            networks=dict, # of tosca.datatypes.network.NetworkInfo
            ports=dict # of tosca.datatypes.network.PortInfo
        )

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

        self.properties.schema.update(
            size=tosca.ScalarSize,
            volume_id=dict(type=str, required=False),
            snapshot_id=dict(type=str, required=False)
        )

        self.capabilities['attachment'] = tosca.capabilities.Attachment()


class SoftwareComponent(Root):
    def __init__(self, name=None):
        super(SoftwareComponent, self).__init__(name)
        from ... import tosca

        self.properties.schema.update(
            component_version=dict(type=tosca.Version, required=False),
            admin_credential=dict(type=tosca.datatypes.Credential, required=False)
        )

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

        self.properties.schema['context_root'] = dict(type=str, required=False)

        self.capabilities['app_endpoint'] = tosca.capabilities.Endpoint()

        self.requirements['host'] = Requirement(
            capability=tosca.capabilities.Container,
            node=tosca.nodes.WebServer,
            relationship=tosca.relationships.HostedOn
        )
