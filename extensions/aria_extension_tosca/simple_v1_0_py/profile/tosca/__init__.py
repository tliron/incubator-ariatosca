
import sys
import inspect
from datetime import datetime

from aria.utils.collections import StrictList
from aria.modeling import models

from ... import get_type_name
from ....simple_v1_0.data_types import (Timestamp, Version, Range, List, Map, ScalarSize,
                                        ScalarTime, ScalarFrequency)


class Type(object):
    ROLE = None


class Template(Type):
    def __init__(self, name=None):
        super(Template, self).__init__()
        self.name = name
        self.description = None

    def validate(self):
        pass


class Topology(Template):
    def __init__(self, name=None):
        super(Topology, self).__init__(name)
        import nodes
        self.node_templates = StrictList(value_class=nodes.NodeTemplate)
        self.groups = []
        self.policies = []

    def validate(self):
        for node in self.node_templates:
            node.validate()
        for group in self.groups:
            group.validate()
        for policy in self.policies:
            policy.validate()

    def create_model(self, context):
        model = models.ServiceTemplate(created_at=datetime.now(),
                                       main_file_name=self.name)

        def get_types(module):
            return tuple(t[1] for t in inspect.getmembers(
                module,
                lambda m: inspect.isclass(m) and issubclass(m, Type))
            )

        def add_types(root, module):
            # TODO: hierarchy
            # TODO: don't add abstract base types
            for the_type in get_types(module):
                type_model = models.Type(name=get_type_name(the_type),
                                         role=the_type.ROLE,
                                         variant=root.variant)
                root.children.append(type_model)

        model.capability_types = models.Type(variant='capability')
        import capabilities
        add_types(model.capability_types, capabilities)
        add_types(model.capability_types, capabilities.network)

        model.interface_types = models.Type(variant='interface')
        import interfaces
        add_types(model.interface_types, interfaces)
        add_types(model.interface_types, interfaces.node)
        add_types(model.interface_types, interfaces.node.lifecycle)
        add_types(model.interface_types, interfaces.relationship)

        model.node_types = models.Type(variant='node')
        import nodes
        add_types(model.node_types, nodes)

        model.relationship_types = models.Type(variant='relationship')
        import relationships
        add_types(model.relationship_types, relationships)
        
        for node_template in self.node_templates:
            node_template_model = node_template.create_model(model)
            model.node_templates[node_template_model.name] = node_template_model

        for node_template in self.node_templates:
            node_template.fix_model(model)
        
        return model


class timestamp(Timestamp):
    def __init__(self, value):
        super(timestamp, self).__init__(None, None, value, None)


class version(Version):
    def __init__(self, value):
        super(version, self).__init__(None, None, value, None)


class range(Range):
    def __init__(self, value1, value2):
        super(range, self).__init__(None, None, [value1, value2], None)


class scalar_unit(object):
    size = None
    time = None
    frequency = None

    
class _scalar_size(ScalarSize):
    def __init__(self, value):
        super(_scalar_size, self).__init__(None, None, value, None)


class _scalar_time(ScalarTime):
    def __init__(self, value):
        super(_scalar_time, self).__init__(None, None, value, None)

    
class _scalar_frequency(ScalarFrequency):
    def __init__(self, value):
        super(_scalar_frequency, self).__init__(None, None, value, None)


scalar_unit.size = _scalar_size
scalar_unit.time = _scalar_time
scalar_unit.frequency = _scalar_frequency

import nodes
import interfaces
import capabilities
import relationships
import datatypes
