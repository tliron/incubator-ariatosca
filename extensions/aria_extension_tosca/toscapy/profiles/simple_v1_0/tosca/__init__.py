
class Template(object):
    def __init__(self, name=None):
        self.name = name


class ServiceTemplate(Template):
    def __init__(self):
        self.node_templates = []


import nodes
import interfaces
import capabilities
import relationships
