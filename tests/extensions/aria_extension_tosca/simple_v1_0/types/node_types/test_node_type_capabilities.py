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

from ... import data

# Syntax

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_node_type_capability_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_capability_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability: {} # "type" is required
""").assert_failure()


def test_node_type_capability_fields(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        description: a description
        properties: {}
        attributes: {}
        valid_source_types: []
        occurrences: [ 0, UNBOUNDED ]
""").assert_success()


# Type

def test_node_type_capability_type_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    capabilities:
      my_capability:
        type: UnknownType
""").assert_failure()


def test_node_type_capability_type_null(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    capabilities:
      my_capability:
        type: null
""").assert_failure()


@pytest.mark.skip(reason='fixed in ARIA-351')
def test_node_type_capability_type_override(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
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


def test_node_type_capability_type_override_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
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


# Parameters

@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_fields(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: string
            description: a description
            default: a value
            status: supported
""", dict(parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_fields_unicode(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  類型: {}
node_types:
  類型:
    capabilities:
      能力:
        type: 類型
        {{ parameter_section }}:
          參數:
            type: string
            description: 描述
            default: 值
            status: supported
""", dict(parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('parameter_section,value', itertools.product(
    data.PARAMETER_SECTION_NAMES,
    data.STATUSES
))
def test_node_type_capability_parameter_status(parser, parameter_section, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: string
            status: {{ value }}
""", dict(parameter_section=parameter_section, value=value)).assert_success()


@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_status_bad(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: string
            status: not a status
""", dict(parameter_section=parameter_section)).assert_failure()


@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_add(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType:
    {{ parameter_section }}:
      my_parameter1:
        type: string
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter2:
            type: string
""", dict(parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_add_default(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: string
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: string
            default: my value
""", dict(parameter_section=parameter_section)).assert_success()


@pytest.mark.skip(reason='fixed in ARIA-351')
@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_type_override(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: {}
capability_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: MyType1
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: MyType2
""", dict(parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('parameter_section', data.PARAMETER_SECTION_NAMES)
def test_node_type_capability_parameter_type_override_bad(parser, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: {}
capability_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: MyType2
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        {{ parameter_section }}:
          my_parameter:
            type: MyType1
""", dict(parameter_section=parameter_section)).assert_failure()


# Valid source types

def test_node_type_capability_valid_source_types(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType1:
    capabilities:
      my_capability:
        type: MyType
        valid_source_types: [ MyType1, MyType2 ]
  MyType2: {}
""").assert_success()


@pytest.mark.parametrize('value', data.NOT_A_LIST)
def test_node_type_capability_valid_source_types_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        valid_source_types: {{ value }}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_capability_valid_source_types_element_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        valid_source_types: [ {{ value }} ]
""", dict(value=value)).assert_failure()


def test_node_type_capability_valid_source_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        valid_source_types: []
""").assert_success()




def test_node_type_capability_valid_source_types_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        valid_source_types: [ UnknownType ]
""").assert_failure()


# Occurrences

@pytest.mark.parametrize('value', data.NOT_OCCURRENCES)
def test_node_type_capability_occurrences(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    capabilities:
      my_capability:
        type: MyType
        occurrences: {{ value }}
""", dict(value=value)).assert_failure()
