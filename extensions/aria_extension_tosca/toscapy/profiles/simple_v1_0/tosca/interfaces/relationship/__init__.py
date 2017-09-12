
from .. import (Root, Operation)


class Configure(Root):
    def __init__(self):
        super(Configure, self).__init__()
        self.operations['pre_configure_source'] = Operation()
        self.operations['pre_configure_target'] = Operation()
        self.operations['post_configure_source'] = Operation()
        self.operations['post_configure_target'] = Operation()
        self.operations['post_configure_target'] = Operation()
        self.operations['add_target'] = Operation()
        self.operations['add_source'] = Operation()
        self.operations['target_changed'] = Operation()
        self.operations['remove_target'] = Operation()
        self.operations['remove_source'] = Operation()
