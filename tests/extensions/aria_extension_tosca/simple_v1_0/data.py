# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Keywords

TYPE_NAMES = ('artifact', 'data', 'capability', 'interface', 'relationship', 'node', 'group',
              'policy')
TYPE_NAME_PLURAL = {
    'artifact': 'artifacts',
    'data': 'datatypes',
    'capability': 'capabilities',
    'interface': 'interfaces',
    'relationship': 'relationships',
    'node': 'nodes',
    'group': 'groups',
    'policy': 'policies'
}
TEMPLATE_NAMES = ('node', 'group', 'policy')
TEMPLATE_NAME_SECTION = {
    'node': 'node_templates',
    'group': 'groups',
    'policy': 'policies'
}
PARAMETER_SECTION_NAMES = ('properties', 'attributes')
PARAMETER_SECTIONS = (
    ('artifact', 'properties'),
    ('data', 'properties'),
    ('capability', 'properties'),
    ('capability', 'attributes'),
    ('interface', 'inputs'),
    ('relationship', 'properties'),
    ('relationship', 'attributes'),
    ('node', 'properties'),
    ('node', 'attributes'),
    ('group', 'properties'),
    ('policy', 'properties')
)


# Values

NOT_A_DICT = ('null', 'a string', '123', '0.123', '[]')
NOT_A_LIST = ('null', 'a string', '123', '0.123', '{}')
NOT_A_STRING = ('123', '0.123', '[]', '{}')
NOT_A_RANGE = NOT_A_LIST + (
    '[]', '[ 1 ]', '[ 1, 2, 3 ]',
    '[ 1, 1 ]', '[ 2, 1 ]',
    '[ 1, a string ]', '[ a string, 1 ]',
    '[ 1.5, 2 ]', '[ 1, 2.5 ]'
)
NOT_OCCURRENCES = NOT_A_RANGE + ('[ -1, 1 ]',)
GOOD_VERSIONS = ("'6.1'", '2.0.1', '3.1.0.beta', "'1.0.0.alpha-10'")
BAD_VERSIONS = ('a_string', '1.2.3.4.5', '1.2.beta', '1.0.0.alpha-x')
STATUSES = ('supported', 'unsupported', 'experimental', 'deprecated')
ENTRY_SCHEMA_VALUES = (
    ('string', 'a string', 'another string'),
    ('integer', '1', '2'),
    ('float', '1.1', '2.2')
)
ENTRY_SCHEMA_VALUES_BAD = (
    ('string', 'a string', '1'),
    ('integer', '1', 'a string'),
    ('float', '1.1', 'a string')
)
