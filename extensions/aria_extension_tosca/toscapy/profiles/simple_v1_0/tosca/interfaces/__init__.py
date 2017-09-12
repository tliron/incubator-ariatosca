
class Interface(object):
    def __init__(self):
        self.operations = {}


class Root(Interface):
    pass


class Operation(object):
    def __init__(self):
        self.implementation = None
        self.dependencies = []


import node
import relationship

