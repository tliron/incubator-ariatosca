
from __future__ import absolute_import  # so we can import standard 'collections'

from aria.utils.type import full_type_name
from aria.utils.collections import OrderedDict
from aria.modeling.functions import Evaluation

from . import get_type_name


class SchemaError(Exception):
    pass


class SchemaKeyError(Exception):
    def __init__(self, key):
        super(SchemaKeyError, self).__init__('unknown key: {0}'.format(key))


class SchemaRequiredKeyError(Exception):
    def __init__(self, key):
        super(SchemaRequiredKeyError, self).__init__('required key has no value: {0}'.format(key))


class SchemaValueError(Exception):
    def __init__(self, key, value, the_type):
        super(SchemaValueError, self).__init__('value for {0} is not a {1}: {2}'
                                               .format(key, full_type_name(the_type), repr(value)))


class SchemaDict(OrderedDict):
    def __init__(self, schema=None):
        super(SchemaDict, self).__init__()
        self.schema = OrderedDict(schema or {})

    def __getitem__(self, key):
        if key not in self.schema:
            raise SchemaKeyError(key)
        return super(SchemaDict, self).__getitem__(key) 

    def __setitem__(self, key, value):
        if key not in self.schema:
            raise SchemaKeyError(key)

        if not hasattr(value, '__call__'):
            schema = self.schema[key]
            if isinstance(schema, dict):
                the_type = schema['type']
            else:
                the_type = schema
            if not isinstance(value, the_type):
                raise SchemaValueError(key, value, the_type)

        return super(SchemaDict, self).__setitem__(key, value) 

    def validate(self):
        pass

    def create_models(self, cls):
        the_models = []
        for name, schema in self.schema.iteritems():
            the_type = schema['type'] if isinstance(schema, dict) else schema
            type_name = get_type_name(the_type)
            value = self.get(name)
            if hasattr(value, '__call__'):
                value = FunctionWrapper(value)
            the_models.append(cls(name=name,
                                  type_name=type_name,
                                  value=value))
        return the_models


class FunctionWrapper(object):
    def __init__(self, func):
        self.func = func
    
    def __evaluate__(self, container_holder):
        return Evaluation(self.func())
        

class RequiredSchemaDict(SchemaDict):
    def validate(self):
        for key, schema in self.schema.iteritems():
            if isinstance(schema, dict):
                required = schema.get('required', True)
            else:
                required = True
            if required and (key not in self):
                raise SchemaRequiredKeyError(key)
