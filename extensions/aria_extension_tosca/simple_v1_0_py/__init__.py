
from aria.utils.type import (full_type_name, BASE_TYPES_TO_CANONICAL_NAMES)
from aria.parser.presentation import Presenter


BASE_NAME =  __name__ + '.profile.'


def get_type_name(cls):
    # TODO: doesn't handle nested classes correctly (e.g. tosca.capabilities._EndpointAdmin)
    name = cls.__module__ + '.' + cls.__name__
    if name.startswith(BASE_NAME):
        return name[len(BASE_NAME):]
    for base_type, canonical_name in BASE_TYPES_TO_CANONICAL_NAMES.iteritems():
        if issubclass(cls, base_type):
            return canonical_name
    return full_type_name(cls)


class ToscaSimplePyPresenter1_0(Presenter):
    DSL_VERSIONS = ('tosca_simple_py_1_0',)
    
    @property
    def topology(self):
        return self._raw['topology']

    def _get_import_locations(self, context):
        return []

    def _get_model(self, context):
        return self.topology.create_model(context)
