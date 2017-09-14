
from .. import Type
from ....collections import RequiredSchemaDict


class Interface(Type):
    def __init__(self):
        super(Interface, self).__init__()
        self.operations = {}
        self.inputs = RequiredSchemaDict()

    def validate(self):
        self.inputs.validate()
        for operation in self.operations.itervalues():
            operation.validate()


class Root(Interface):
    pass


class Operation(object):
    def __init__(self):
        self.implementation = None
        self.dependencies = []
        self.inputs = RequiredSchemaDict()

    def validate(self):
        self.inputs.validate()


import node
import relationship

