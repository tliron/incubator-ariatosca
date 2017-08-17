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


# Syntax

@pytest.mark.parametrize('value', ('null', 'a_string', '123', '0.123', '[]'))
def test_metadata_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata: {{ value }}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('field,value', (
    ('template_name', '123'),
    ('template_name', '0.123'),
    ('template_name', '[]'),
    ('template_name', '{}'),
    ('template_author', '123'),
    ('template_author', '0.123'),
    ('template_author', '[]'),
    ('template_author', '{}'),
    ('template_version', '123'),
    ('template_version', '0.123'),
    ('template_version', '[]'),
    ('template_version', '{}')))
def test_metadata_normative_wrong_yaml_type(parser, field, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
    {{ field }}: {{ value }}
""", dict(field=field, value=value)).assert_failure()


@pytest.mark.parametrize('value', ('123', '0.123', '[]', '{}'))
def test_metadata_non_normative_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
    non_normative: {{ value }}
""", dict(value=value)).assert_failure()


def test_metadata_empty_dict(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata: {}
""").assert_success()


# Normative

@pytest.mark.parametrize('value', ('null', 'a_string', '1.2.3.4.5'))
def test_metadata_normative_template_bad_version(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
    template_version: {{ value }}
""", dict(value=value)).assert_failure()


@pytest.mark.parametrize('value', ("'6.1'", '2.0.1', '3.1.0.beta', "'1.0.0.alpha-10'"))
def test_metadata_normative_template_version(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
    template_version: {{ value }}
""", dict(value=value)).assert_success()

# Non-normative

def test_metadata_with_non_normative_fields(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
  template_name: name
  template_author: author
  template_version: 1.0.0.beta
  non_normative1: non_normative1
  non_normative2: non_normative2
  non_normative3: non_normative3
""").assert_success()


def test_metadata_with_non_normative_fields_nulls(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
  template_name: null
  template_author: null
  template_version: 1.0.0.beta
  non_normative1: null
  non_normative2: null
  non_normative3: null
""").assert_success()


def test_metadata_with_non_normative_fields_unicode(parser):
    parser.parse_literal(u"""
tosca_definitions_version: tosca_simple_yaml_1_0
metadata:
  template_name: 詠嘆調
  template_author: 詠嘆調
  template_version: 1.0.0.詠嘆調
  non_normative1: 詠嘆調
  non_normative2: 詠嘆調
  non_normative3: 詠嘆調
""").assert_success()
