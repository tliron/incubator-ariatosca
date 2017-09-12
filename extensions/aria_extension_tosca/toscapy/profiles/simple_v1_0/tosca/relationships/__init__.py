
from .....collections import (SchemaDict, RequiredSchemaDict)


class Relationship(object):
    def __init__(self):
        self.properties = RequiredSchemaDict()
        self.attributes = SchemaDict()
        self.interfaces = {}
        self.valid_target_types = []


class Root(Relationship):
    def __init__(self):
        super(Root, self).__init__()
        from ... import tosca

        self.attributes.schema['tosca_id'] = str
        self.attributes.schema['tosca_name'] = str
        self.attributes.schema['state'] = str
        self.attributes['state'] = 'initial'

        self.interfaces['Configure'] = tosca.interfaces.relationship.Configure()


class DependsOn(Root):
    def __init__(self):
        super(DependsOn, self).__init__()
        from ... import tosca

        self.valid_target_types.append(tosca.capabilities.Node)


class HostedOn(Root):
    def __init__(self):
        super(HostedOn, self).__init__()
        from ... import tosca

        self.valid_target_types.append(tosca.capabilities.Container)


class AttachesTo(Root):
    def __init__(self):
        super(AttachesTo, self).__init__()
        from ... import tosca

        self.properties.schema['location'] = {'type': str, 'required': True}
        self.properties.schema['device'] = str

        self.attributes.schema['device'] = str

        self.valid_target_types.append(tosca.capabilities.Attachment)
