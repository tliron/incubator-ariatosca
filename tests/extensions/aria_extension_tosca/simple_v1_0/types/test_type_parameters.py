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


# Fields

@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_fields(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: string
        description: a description
        default: a value
        status: supported
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_fields_unicode(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      參數:
        type: string
        description: 描述
        default: 值
        status: supported
""", dict(name=name, parameter_section=parameter_section)).assert_success()


# Status

@pytest.mark.parametrize(
    'name,parameter_section,value',
    ((s[0], s[1], v)
     for s, v in itertools.product(data.PARAMETER_SECTIONS, data.STATUSES))
)
def test_node_type_parameter_status(parser, name, parameter_section, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: string
        status: {{ value }}
""", dict(name=name, parameter_section=parameter_section, value=value)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_status_bad(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    {{ parameter_section }}:
      my_parameter:
        type: string
        status: not a status
""", dict(name=name, parameter_section=parameter_section)).assert_failure()


# Overriding

@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_add(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType1:
    {{ parameter_section }}:
      my_parameter1:
        type: string
  MyType2:
    derived_from: MyType1
    {{ parameter_section }}:
      my_parameter2:
        type: string
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_add_default(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType1:
    {{ parameter_section }}:
      my_parameter:
        type: string
  MyType2:
    derived_from: MyType1
    {{ parameter_section }}:
      my_parameter:
        type: string
        default: my value 
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.skip(reason='fixed in ARIA-351')
@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_type_override(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
{{ name }}_types:
  MyType1:
    {{ parameter_section }}:
      my_parameter:
        type: MyType1
  MyType2:
    derived_from: MyType1
    {{ parameter_section }}:
      my_parameter:
        type: MyType2
""", dict(name=name, parameter_section=parameter_section)).assert_success()


@pytest.mark.parametrize('name,parameter_section', data.PARAMETER_SECTIONS)
def test_node_type_parameter_type_override_bad(parser, name, parameter_section):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
data_types:
  MyType1: {}
  MyType2:
    derived_from: MyType1
{{ name }}_types:
  MyType1:
    {{ parameter_section }}:
      my_parameter:
        type: MyType2
  MyType2:
    derived_from: MyType1
    {{ parameter_section }}:
      my_parameter:
        type: MyType1
""", dict(name=name, parameter_section=parameter_section)).assert_failure()
