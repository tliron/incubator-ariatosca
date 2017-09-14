
from aria.modeling import models

from .. import Type
from .... import get_type_name
from ....collections import (SchemaDict, RequiredSchemaDict)


class Capability(Type):
    def __init__(self):
        super(Capability, self).__init__()
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.valid_source_types = []
        self.min_occurrences = 0
        self.max_occurrences = None

    def validate(self):
        self.properties.validate()

    def create_model(self, service_template):
        capability_type = \
            service_template.capability_types.get_descendant(get_type_name(self.__class__))
        model = models.CapabilityTemplate(type=capability_type,
                                          min_occurrences=self.min_occurrences,
                                          max_occurrences=self.max_occurrences)
        for prop in self.properties.create_models(models.Property):
            model.properties[prop.name] = prop
        #for attribute in self.attributes.create_models(models.Attribute):
        #    model.attributes[attribute.name] = attribute
        return model


class Root(Capability):
    pass


class Node(Root):
    pass


class Container(Root):
    def __init__(self):
        super(Container, self).__init__()
        from ... import tosca

        self.properties.schema.update(
            num_cpus=dict(type=int, required=False),
            cpu_frequency=dict(type=tosca.ScalarFrequency, required=False),
            disk_size=dict(type=tosca.ScalarSize, required=False),
            mem_size=dict(type=tosca.ScalarSize, required=False)
        )


class OperatingSystem(Root):
    def __init__(self):
        super(OperatingSystem, self).__init__()

        self.properties.schema.update(
            architecture=dict(type=str, required=False),
            type=dict(type=str, required=False),
            distribution=dict(type=str, required=False),
            version=dict(type=str, required=False)
        )


class Scalable(Root):
    def __init__(self):
        super(Scalable, self).__init__()

        self.properties.schema.update(
            min_instances=int,
            max_instances=int,
            default_instances=dict(type=int, required=False)
        )
        self.properties.update(
            min_instances=1,
            max_instances=1
        )


class Attachment(Root):
    pass


class Endpoint(Root):
    Admin = None

    def __init__(self):
        super(Endpoint, self).__init__()
        from ... import tosca

        self.properties.schema.update(
            protocol=str,
            port=dict(type=tosca.datatypes.network.PortDef, required=False),
            secure=dict(type=bool, required=False),
            url_path=dict(type=str, required=False),
            port_name=dict(type=str, required=False),
            network_name=dict(type=str, required=False),
            initiator=dict(type=str, required=False),
            ports=dict(type=dict, required=False) # of tosca.datatypes.network.PortSpec
        )
        self.properties.update(
            protocol='tcp',
            secure=False
        )

        self.attributes.schema['ip_address'] = str


class _EndpointAdmin(Endpoint):
    def __init__(self):
        super(_EndpointAdmin, self).__init__()

        self.properties['secure'] = True


Endpoint.Admin = _EndpointAdmin


import network
