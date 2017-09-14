
from ... import (Root, Operation)


class Standard(Root):
    def __init__(self):
        super(Standard, self).__init__()
        self.operations.update(
            create=Operation(),
            configure=Operation(),
            start=Operation(),
            stop=Operation(),
            delete=Operation()
        )
