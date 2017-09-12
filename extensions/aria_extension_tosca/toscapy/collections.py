
from __future__ import absolute_import  # so we can import standard 'collections'

from aria.utils.type import full_type_name


class SchemaError(Exception):
    pass


class SchemaKeyError(Exception):
    def __init__(self, key):
        super(SchemaKeyError, self).__init__('unknown key: {0}'.format(key))


class SchemaRequiredKeyError(Exception):
    def __init__(self, key):
        super(SchemaKeyError, self).__init__('required key has no value: {0}'.format(key))


class SchemaValueError(Exception):
    def __init__(self, key, value, the_type):
        super(SchemaValueError, self).__init__('value for {0} is not a {1}: {2}'
                                               .format(key, full_type_name(the_type), repr(value)))



class SchemaDict(dict):
    def __init__(self, schema=None):
        super(SchemaDict, self).__init__()
        self.schema = schema or {}

    def __getitem__(self, key):
        if key not in self.schema:
            raise SchemaKeyError(key)
        return super(SchemaDict, self).__getitem__(key) 

    def __setitem__(self, key, value):
        if key not in self.schema:
            raise SchemaKeyError(key)

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


class RequiredSchemaDict(SchemaDict):
    def validate(self):
        for key, schema in self.schema.iteritems():
            if isinstance(schema, dict):
                required = schema['required'] or False
                if required and (key not in self):
                    raise SchemaRequiredKeyError(key)
