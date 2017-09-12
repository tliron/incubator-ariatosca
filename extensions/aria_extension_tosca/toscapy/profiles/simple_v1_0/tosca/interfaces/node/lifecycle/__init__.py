
from ... import (Root, Operation)


class Standard(Root):
    def __init__(self):
        super(Standard, self).__init__()
        self.operations['create'] = Operation()
        self.operations['configure'] = Operation()
        self.operations['start'] = Operation()
        self.operations['stop'] = Operation()
        self.operations['delete'] = Operation()
