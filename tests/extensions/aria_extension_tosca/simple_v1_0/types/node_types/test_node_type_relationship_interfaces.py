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

"""
Developer note: make sure that these tests mirror those in test_type_interfaces.py.
"""

import pytest

from ... import data


# Syntax

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_node_type_relationship_interface_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_relationship_interface_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface: {} # "type" is required
""").assert_failure()


def test_node_type_relationship_interface_fields(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                inputs: {}
                my_operation1: {}
                my_operation2: {}
""").assert_success()


def test_node_type_relationship_interface_fields_unicode(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  類型: {}
relationship_types:
  類型: {}
interface_types:
  類型: {}
node_types:
  類型:
    requirements:
      - 需求:
          capability: 類型
          relationship:
            type: 類型
            interfaces:
              接口:
                type: 類型
                手術:
                  implementation: 履行
""").assert_success()


# Type

def test_node_type_relationship_interface_type_override1(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType1
interface_types:
  MyType1: {}
  MyType2:
    derived_form: MyType1
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType2
""").assert_success()


def test_node_type_relationship_interface_type_override2(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType1: {}
  MyType2:
    derived_form: MyType1
node_types:
  MyType1:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType1
  MyType2:
    derived_from: MyType1
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType2
""").assert_success()


@pytest.mark.skip(reason='fix')
def test_node_type_relationship_interface_type_override1_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType:
    interfaces:
      my_interface:
        type: MyType2
interface_types:
  MyType1: {}
  MyType2:
    derived_form: MyType1
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType1
""").assert_failure()


@pytest.mark.skip(reason='fix')
def test_node_type_relationship_interface_type_override2_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType1: {}
  MyType2:
    derived_form: MyType1
node_types:
  MyType1:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType2
  MyType2:
    derived_from: MyType1
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType1
""").assert_failure()


# Interface inputs

def test_node_type_relationship_interface_inputs_add(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                inputs:
                  my_input2:
                    type: string
""").assert_success()


def test_node_type_relationship_interface_inputs_type_override_same(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType:
    inputs:
      my_input:
        type: string
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                inputs:
                  my_input:
                    type: string
""").assert_success()


def test_node_type_relationship_interface_inputs_type_override_derived(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input:
        type: MyType1
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                inputs:
                  my_input:
                    type: MyType2
""").assert_success()


@pytest.mark.skip(reason='fix')
def test_node_type_relationship_interface_inputs_type_override_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input:
        type: MyType2
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                inputs:
                  my_input:
                    type: MyType1
""").assert_failure()


# Operations

def test_node_type_relationship_interface_operation_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation: {}
""").assert_success()


def test_node_type_relationship_interface_operation_fields(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  description: a description
                  implementation: {}
                  inputs: {}
""").assert_success()


# Operation implementation

def test_node_type_relationship_interface_operation_implementation_short_form(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  implementation: an implementation
""").assert_success()


def test_node_type_relationship_interface_operation_implementation_long_form(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  implementation:
                    primary: an implementation
                    dependencies:
                      - a dependency
                      - another dependency
""").assert_success()


@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_relationship_interface_operation_implementation_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  implementation:
                    primary: {{ value }}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('value', data.NOT_A_STRING)
def test_node_type_relationship_interface_operation_dependencies_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  implementation:
                    primary: an implementation
                    dependencies:
                      - {{ value }}
""", dict(value=value)).assert_failure()


# Operation inputs

def test_node_type_relationship_interface_operation_inputs_add(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType:
    inputs:
      my_input1:
        type: string
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  inputs:
                    my_input2:
                      type: string
""").assert_success()


def test_node_type_relationship_interface_operation_inputs_override_same_type(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
interface_types:
  MyType:
    inputs:
      my_input:
        type: string
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  inputs:
                    my_input:
                      type: string
""").assert_success()


def test_node_type_relationship_interface_operation_inputs_override_derived_type(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input:
        type: MyType1
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  inputs:
                    my_input:
                      type: MyType2
""").assert_success()


@pytest.mark.skip(reason='fix')
def test_node_type_relationship_interface_operation_inputs_override_bad(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType: {}
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
interface_types:
  MyType:
    inputs:
      my_input:
        type: MyType2
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType
            interfaces:
              my_interface:
                type: MyType
                my_operation:
                  inputs:
                    my_input:
                      type: MyType1
""").assert_failure()
