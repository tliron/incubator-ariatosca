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


SECTIONS = (
    ('artifact', 'properties'),
    ('data', 'properties'),
    ('capability', 'properties'),
    ('capability', 'attributes'),
    ('relationship', 'properties'),
    ('relationship', 'attributes'),
    ('node', 'properties'),
    ('node', 'attributes'),
    ('group', 'properties'),
    ('policy', 'properties')
)
SECTION_NAMES = ('properties', 'attributes')
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


# Fields

@pytest.mark.parametrize('name,parameter_section', SECTIONS)
def test_node_type_parameter_fields(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_param:
        type: string
        description: a description
        default: a value
        status: supported
""", dict(name=name, parameter_section=parameter_section)).assert_success()


# Status

@pytest.mark.parametrize(
    'name,parameter_section,value',
    ((s[0], s[1], v)
     for s, v in itertools.product(SECTIONS, data.STATUSES))
)
def test_node_type_parameter_status_good(parser, name, parameter_section, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_param:
        type: string
        status: {{ value }}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_success()


@pytest.mark.parametrize('name,parameter_section', SECTIONS)
def test_node_type_parameter_status_bad(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_param:
        type: string
        status: bad
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Entry schema

@pytest.mark.parametrize('section,values', itertools.product(
    SECTION_NAMES,
    ENTRY_SCHEMA_VALUES
))
def test_node_type_parameter_map(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_param:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_param:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(section=section, values=values)).assert_success()


@pytest.mark.parametrize('section,values', itertools.product(
    SECTION_NAMES,
    ENTRY_SCHEMA_VALUES_BAD
))
def test_node_type_parameter_map_bad(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_param:
        type: map
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_param:
          key1: {{ values[1] }}
          key2: {{ values[2] }}
""", dict(section=section, values=values)).assert_failure()


@pytest.mark.parametrize('section,values', itertools.product(
    SECTION_NAMES,
    ENTRY_SCHEMA_VALUES
))
def test_node_type_parameter_list(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_param:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_param:
          - {{ values[1] }}
          - {{ values[2] }}
""", dict(section=section, values=values)).assert_success()


@pytest.mark.parametrize('section,values', itertools.product(
    SECTION_NAMES,
    ENTRY_SCHEMA_VALUES_BAD
))
def test_node_type_parameter_list_bad(parser, section, values):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    {{ section }}:
      my_param:
        type: list
        entry_schema: {{ values[0] }}
topology_template:
  node_templates:
    my_template:
      type: MyType
      {{ section }}:
        my_param:
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


# Overriding

@pytest.mark.parametrize('section', SECTION_NAMES)
def test_node_type_parameter_override_add_default(parser, section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType1:
    {{ section }}:
      my_param:
        type: string
  MyType2:
    derived_from: MyType1
    {{ section }}:
      my_param:
        type: string
        default: my value 
""", dict(section=section)).assert_success()


@pytest.mark.skip(reason='fixed in ARIA-351')
@pytest.mark.parametrize('section', ('properties', 'attributes'))
def test_node_type_parameter_override_change_type_good(parser, section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1:
    properties:
      field1:
        type: string
  MyType2:
    derived_from: MyType1
    properties:
      field2:
        type: integer
node_types:
  MyType1:
    {{ section }}:
      my_param:
        type: MyType1
  MyType2:
    derived_from: MyType1
    {{ section }}:
      my_param:
        type: MyType2
""", dict(section=section)).assert_success()


@pytest.mark.parametrize('section', ('properties', 'attributes'))
def test_node_type_parameter_override_change_type_bad(parser, section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1:
    properties:
      field1:
        type: string
  MyType2:
    derived_from: MyType1
    properties:
      field2:
        type: integer
node_types:
  MyType1:
    {{ section }}:
      my_param:
        type: MyType2
  MyType2:
    derived_from: MyType1
    {{ section }}:
      my_param:
        type: MyType1
""", dict(section=section)).assert_failure()
