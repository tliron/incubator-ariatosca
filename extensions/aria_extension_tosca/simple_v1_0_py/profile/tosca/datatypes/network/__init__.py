
from .. import Root


class NetworkInfo(Root):
    def __init__(self, data=None):
        super(NetworkInfo, self).__init__(dict(
            network_name=dict(type=str, required=False),
            network_id=dict(type=str, required=False),
            addresses=dict(type=list, required=False) # of str
        ))
        if data is not None:
            self.update(data)


class PortInfo(Root):
    def __init__(self, data=None):
        super(PortInfo, self).__init__(dict(
            port_name=dict(type=str, required=False),
            port_id=dict(type=str, required=False),
            network_id=dict(type=str, required=False),
            mac_address=dict(type=str, required=False),
            addresses=dict(type=list, required=False) # of str
        ))
        if data is not None:
            self.update(data)


class PortDef(int):
    pass
