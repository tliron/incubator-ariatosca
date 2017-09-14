
from .. import (Root, Operation)


class Configure(Root):
    def __init__(self):
        super(Configure, self).__init__()
        self.operations.update(
            pre_configure_source=Operation(),
            pre_configure_target=Operation(),
            post_configure_source=Operation(),
            post_configure_target=Operation(),
            add_target=Operation(),
            add_source=Operation(),
            target_changed=Operation(),
            remove_target=Operation(),
            remove_source=Operation()
        )
