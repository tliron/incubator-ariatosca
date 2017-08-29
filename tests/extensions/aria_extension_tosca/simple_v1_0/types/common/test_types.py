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

@pytest.mark.parametrize('name,value', itertools.product(
    data.TYPE_NAMES,
    data.NOT_A_DICT
))
def test_type_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType: {{ value }}
""", dict(name=name, value=value)).assert_failure()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_empty(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType: {}
""", dict(name=name)).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TYPE_NAMES,
    data.NOT_A_STRING
))
def test_type_derived_from_wrong_yaml_type(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: {{ value }}
""", dict(name=name, value=value)).assert_failure()


# Derivation

@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_derived_from_unknown(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: UnknownType
""", dict(name=name)).assert_failure()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_derived_from_null(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: null
""", dict(name=name)).assert_failure()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_derived_from_self(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: MyType
""", dict(name=name)).assert_failure()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_derived_from_circular(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType1:
    derived_from: MyType3
  MyType2:
    derived_from: MyType1
  MyType3:
    derived_from: MyType2
""", dict(name=name)).assert_failure()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_derived_from_root(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: tosca.{{ plural }}.Root
""", dict(name=name, plural=data.TYPE_NAME_PLURAL[name])).assert_success()


# Common fields

@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_fields(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    derived_from: tosca.{{ plural }}.Root
    version: 1.0.0
    description: a description
""", dict(name=name, plural=data.TYPE_NAME_PLURAL[name])).assert_success()


@pytest.mark.parametrize('name', data.TYPE_NAMES)
def test_type_fields_unicode(parser, name):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  類型:
    derived_from: tosca.{{ plural }}.Root
    version: 1.0.0.詠嘆調-10
    description: 描述
""", dict(name=name, plural=data.TYPE_NAME_PLURAL[name])).assert_success()


@pytest.mark.parametrize('name,value', itertools.product(
    data.TYPE_NAMES,
    data.BAD_VERSIONS
))
def test_type_bad_version(parser, name, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
{{ name }}_types:
  MyType:
    version: {{ value }}
""", dict(name=name, value=value)).assert_failure()
