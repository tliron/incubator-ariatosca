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


TYPE_NAMES = ('node', 'relationship', 'group')


# Syntax

@pytest.mark.parametrize('name,value', itertools.product(
    TYPE_NAMES,
    data.NOT_A_DICT
))
def test_type_interface_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface: {{ value }}
""", dict(name=name, value=value)).assert_failure()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    interfaces:
      my_interface: {} # "type" is required
""", dict(name=name)).assert_failure()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_fields(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        inputs: {}
        operation1: {}
        operation2: {}
""", dict(name=name)).assert_success()


# Type

@pytest.mark.skip(reason='fixed in ARIA-351')
@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_type_override_good(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType1: {}
  MyType2: {}
{{ name }}_types:
  MyType1:
    interfaces:
      my_interface:
        type: MyType1
  MyType2:
    derived_from: MyType1
    interfaces:
      my_interface:
        type: MyType2
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_type_override_bad(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType1: {}
  MyType2: {}
{{ name }}_types:
  MyType1:
    interfaces:
      my_interface:
        type: MyType2
  MyType2:
    derived_from: MyType1
    interfaces:
      my_interface:
        type: MyType1
""", dict(name=name)).assert_failure()


# Interface inputs

@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_inputs_add(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        inputs:
          my_input2:
            type: string
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_inputs_type_override_same(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        inputs:
          my_input1:
            type: string
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_inputs_type_override_derived(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input1:
        type: MyType1
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        inputs:
          my_input1:
            type: MyType2
""", dict(name=name)).assert_success()


@pytest.mark.skip(reason='fix')
@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_inputs_type_override_bad(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2: {}
interface_types:
  MyType:
    inputs:
      my_input1:
        type: MyType2
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        inputs:
          my_input1:
            type: MyType1
""", dict(name=name)).assert_failure()


# Operations

@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1: {}
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_fields(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          description: a description
          implementation: {}
          inputs: {}
""", dict(name=name)).assert_success()


# Operation implementation

@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_implementation_short_form(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          implementation: an implementation
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_implementation_long_form(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          implementation:
            primary: an implementation
            dependencies:
              - a dependency
              - another dependency
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    TYPE_NAMES,
    data.NOT_A_STRING
))
def test_type_interface_operation_implementation_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          implementation:
            primary: {{ value }}
""", dict(name=name, value=value)).assert_failure()


@pytest.mark.parametrize('name,value', itertools.product(
    TYPE_NAMES,
    data.NOT_A_STRING
))
def test_type_interface_operation_dependencies_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType: {}
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          implementation:
            primary: an implementation
            dependencies:
              - {{ value }}
""", dict(name=name, value=value)).assert_failure()


# Operation inputs

@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_inputs_add(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          inputs:
            my_input2:
              type: string
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_inputs_override_same_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          inputs:
            my_input1:
              type: string
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_inputs_override_derived_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input1:
        type: MyType1
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          inputs:
            my_input1:
              type: MyType2
""", dict(name=name)).assert_success()


@pytest.mark.skip(reason='fix')
@pytest.mark.parametrize('name', TYPE_NAMES)
def test_type_interface_operation_inputs_override_bad(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input1:
        type: MyType2
{{ name }}_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType
        operation1:
          inputs:
            my_input1:
              type: MyType1
""", dict(name=name)).assert_failure()
