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

import pytest


# Overriding

@pytest.mark.skip(reason='fixed in ARIA-351')
def test_node_type_capability_override_change_type_good(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType1:
    properties:
      prop1:
        type: string
  MyType2:
    derived_from: MyType1
    properties:
      prop2:
        type: integer
node_types:
  MyType1:
    capabilities:
      my_capability:
        type: MyType1
  MyType2:
    derived_from: MyType1
    capabilities:
      my_capability:
        type: MyType2
""").assert_success()


def test_node_type_capability_override_change_type_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType1:
    properties:
      prop1:
        type: string
  MyType2:
    derived_from: MyType1
    properties:
      prop2:
        type: integer
node_types:
  MyType1:
    capabilities:
      my_capability:
        type: MyType2
  MyType2:
    derived_from: MyType1
    capabilities:
      my_capability:
        type: MyType1
""").assert_failure()
