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

from . import data


# Syntax

@pytest.mark.parametrize('value', data.NOT_A_DICT)
def test_topology_template_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template: {{ value }}
""", dict(value=value)).assert_failure()


def test_topology_template_emtpy(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template: {}
""").assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_NAMES,
    data.NOT_A_DICT
))
def test_template_section_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}: {{ value }}
""", dict(section=data.TEMPLATE_NAME_SECTION[name], value=value)).assert_failure()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TEMPLATE_NAMES,
    data.NOT_A_STRING
))
def test_template_type_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}:
    my_template:
      type: {{ value }}
""", dict(section=data.TEMPLATE_NAME_SECTION[name], value=value)).assert_failure()


# Common fields

@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_template_fields(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}:
    my_template:
      type: tosca.{{ plural }}.Root
      description: a description
""", dict(section=data.TEMPLATE_NAME_SECTION[name],
          plural=data.TYPE_NAME_PLURAL[name])).assert_success()


# Of types

@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_template_of_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
    MyType: {}
topology_template:
  {{ section }}:
    my_template:
      type: MyType
""", dict(name=name, section=data.TEMPLATE_NAME_SECTION[name])).assert_success()


@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_template_of_type_unicode(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
    類型: {}
topology_template:
  {{ section }}:
    模板:
      type: 類型
""", dict(name=name, section=data.TEMPLATE_NAME_SECTION[name])).assert_success()


@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_template_of_unknown_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}:
    my_template:
      type: UnknownType
""", dict(section=data.TEMPLATE_NAME_SECTION[name])).assert_failure()


@pytest.mark.parametrize('name', data.TEMPLATE_NAMES)
def test_template_of_null_type(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
topology_template:
  {{ section }}:
    my_template:
      type: null
""", dict(section=data.TEMPLATE_NAME_SECTION[name])).assert_failure()
