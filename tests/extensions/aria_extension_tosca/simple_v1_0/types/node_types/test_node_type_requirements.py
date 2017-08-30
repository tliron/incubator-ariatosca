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

from ... import data


# Syntax

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_node_type_requirement_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    requirements:
      - my_requirement: {{ value }}
""", dict(value=value)).assert_failure()


def test_node_type_requirement_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    requirements:
      - my_requirement: {} # "capability" is required
""").assert_failure()


def test_node_type_requirement_fields(parser):
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
          node: MyType
          relationship:
            type: MyType
          occurrences: [ 0, UNBOUNDED ]
""").assert_success()


def test_node_type_requirement_fields_unicode(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  類型: {}
relationship_types:
  類型: {}
node_types:
  類型:
    requirements:
      - 需求:
          capability: 類型
          node: 類型
          relationship:
            type: 類型
          occurrences: [ 0, UNBOUNDED ]
""").assert_success()


# Capability

def test_node_type_requirement_capability_short_form(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement: MyType
""").assert_success()


def test_node_type_requirement_capability_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: UnknownType
""").assert_failure()


def test_node_type_requirement_capability_null(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: null
""").assert_failure()


def test_node_type_requirement_capability_override(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType1: {}
  MyType2: {}
node_types:
  MyType1:
    requirements:
      - my_requirement:
          capability: MyType1
  MyType2:
    derived_from: MyType1
    requirements:
      - my_requirement:
          capability: MyType2 # you are allowed to change the capability type to anything
""").assert_success()


# Node

def test_node_type_requirement_node_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          node: UnknownType
""").assert_failure()


def test_node_type_requirement_node_null(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          node: null
""").assert_failure()


def test_node_type_requirement_node_override(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType1:
    requirements:
      - my_requirement:
          capability: MyType
          node: MyType3
  MyType2:
    derived_from: MyType1
    requirements:
      - my_requirement:
          capability: MyType
          node: MyType4 # you are allowed to change the node type to anything
  MyType3: {}
  MyType4: {}
""").assert_success()


# Relationship

def test_node_type_requirement_relationship_type_unknown(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: UnknownType
""").assert_failure()


def test_node_type_requirement_relationship_type_null(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: null
""").assert_failure()


def test_node_type_requirement_relationship_type_override(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
relationship_types:
  MyType1: {}
  MyType2: {}
node_types:
  MyType1:
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType1
  MyType2:
    derived_from: MyType1
    requirements:
      - my_requirement:
          capability: MyType
          relationship:
            type: MyType2 # you are allowed to change the relationship type to anything
""").assert_success()


# Occurrences

@pytest.mark.parametrize('value', data.NOT_OCCURRENCES)
def test_node_type_requirement_occurrences(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
capability_types:
  MyType: {}
node_types:
  MyType:
    requirements:
      - my_requirement:
          type: MyType
          occurrences: {{ value }}
""", dict(value=value)).assert_failure()
