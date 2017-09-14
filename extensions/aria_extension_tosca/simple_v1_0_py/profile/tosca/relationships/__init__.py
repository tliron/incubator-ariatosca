
from .. import Type
from ....collections import (SchemaDict, RequiredSchemaDict)


class Relationship(Type):
    def __init__(self):
        super(Relationship, self).__init__()
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.interfaces = {}
        self.valid_target_types = []


class Root(Relationship):
    def __init__(self):
        super(Root, self).__init__()
        from ... import tosca

        self.attributes.schema.update(
            tosca_id=str,
            tosca_name=str,
            state=str,
        )
        self.attributes['state'] = 'initial'

        self.interfaces['Configure'] = tosca.interfaces.relationship.Configure()


class DependsOn(Root):
    def __init__(self):
        super(DependsOn, self).__init__()
        from ... import tosca

        self.valid_target_types.append(tosca.capabilities.Node)


class HostedOn(Root):
    ROLE = 'host'
    
    def __init__(self):
        super(HostedOn, self).__init__()
        from ... import tosca

        self.valid_target_types.append(tosca.capabilities.Container)


class AttachesTo(Root):
    def __init__(self):
        super(AttachesTo, self).__init__()
        from ... import tosca

        self.properties.update(
            location=str,
            device=dict(type=str, required=False)
        )

        self.attributes.schema['device'] = str

        self.valid_target_types.append(tosca.capabilities.Attachment)
