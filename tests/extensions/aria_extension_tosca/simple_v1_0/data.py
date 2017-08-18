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


NOT_A_DICT = ('null', 'a string', '123', '0.123', '[]')
NOT_A_LIST = ('null', 'a string', '123', '0.123', '{}')
NOT_A_STRING = ('123', '0.123', '[]', '{}')
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
GOOD_VERSIONS = ("'6.1'", '2.0.1', '3.1.0.beta', "'1.0.0.alpha-10'")
BAD_VERSIONS = ('a_string', '1.2.3.4.5', '1.2.beta', '1.0.0.alpha-x')
