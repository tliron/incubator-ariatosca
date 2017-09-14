
from ....collections import RequiredSchemaDict


class DataType(RequiredSchemaDict):
    def __init__(self, schema=None):
        super(DataType, self).__init__(schema)


class Root(DataType):
    pass


class Credential(Root):
    def __init__(self, data=None):
        super(Credential, self).__init__(dict(
            protocol=dict(type=str, required=False),
            token_type=dict(type=str, required=False),
            token=dict(type=str, required=False),
            keys=dict(type=dict, required=False), # of str
            user=dict(type=str, required=False)
        ))
        self['token_type'] = 'password'
        if data is not None:
            self.update(data)


import network
