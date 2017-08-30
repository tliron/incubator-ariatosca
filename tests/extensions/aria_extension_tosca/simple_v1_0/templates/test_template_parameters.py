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

import itertools

import pytest

from .. import data


# Entry schema

@pytest.mark.parametrize('section,values', itertools.product(
    data.PARAMETER_SECTION_NAMES,
    data.ENTRY_SCHEMA_VALUES
))
def test_node_type_parameter_map(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_parameter:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_parameter:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(section=section, values=values)).assert_success()


@pytest.mark.parametrize('section,values', itertools.product(
    data.PARAMETER_SECTION_NAMES,
    data.ENTRY_SCHEMA_VALUES_BAD
))
def test_node_type_parameter_map_bad(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_parameter:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_parameter:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(section=section, values=values)).assert_failure()


@pytest.mark.parametrize('section,values', itertools.product(
    data.PARAMETER_SECTION_NAMES,
    data.ENTRY_SCHEMA_VALUES
))
def test_node_type_parameter_list(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_parameter:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_parameter:
          - {{ values[1] }}
          - {{ values[2] }}
""", dict(section=section, values=values)).assert_success()


@pytest.mark.parametrize('section,values', itertools.product(
    data.PARAMETER_SECTION_NAMES,
    data.ENTRY_SCHEMA_VALUES_BAD
))
def test_node_type_parameter_list_bad(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_parameter:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_parameter:
          - {{ values[1] }}
          - {{ values[2] }}
""", dict(section=section, values=values)).assert_failure()


# Required

@pytest.mark.skip(reason='fixed in ARIA-351')
def test_node_type_property_required(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    properties:
      my_property:
        type: string
topology_template:
  node_templates:
    my_template:
      type: MyType
""").assert_failure()


def test_node_type_property_not_required(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    properties:
      my_property:
        type: string
        required: false
topology_template:
  node_templates:
    my_template:
      type: MyType
""").assert_success()


def test_node_type_property_required_with_default(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    properties:
      my_property:
        type: string
        default: a string
topology_template:
  node_templates:
    my_template:
      type: MyType
""").assert_success()
