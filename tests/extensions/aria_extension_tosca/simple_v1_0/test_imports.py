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

from . import data
from ....mechanisms.web_server import WebServer


# Fixtures

NODE_TYPE_IMPORT = """
node_types:
  MyNode:
    derived_from: tosca.nodes.Root
"""

BAD_IMPORT = """
node_types:
  MyNode:
    derived_from: not.a.node.type
"""

@pytest.fixture(scope='session')
def repository():
    repository = WebServer()
    repository.add_text_yaml('/imports/node-type.yaml', NODE_TYPE_IMPORT)
    repository.add_text_yaml('/imports/{0}.yaml'.format(WebServer.escape('節點類型')),
                             NODE_TYPE_IMPORT)
    repository.add_text_yaml('/imports/bad.yaml', BAD_IMPORT)
    with repository:
        yield repository.root


# Syntax

@pytest.mark.parametrize('value', data.NOT_A_LIST)
def test_imports_wrong_yaml_type(parser, value):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports: {{ value }}
""", dict(value=value)).assert_failure()


def test_imports_empty(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports: []
""").assert_success()


# Variants

def test_import_single_short_form(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - {{ repository }}/imports/node-type.yaml
topology_template:
  node_templates:
    my_node:
      type: MyNode
""", dict(repository=repository)).assert_success()


def test_import_single_short_form_unicode(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - {{ repository }}/imports/節點類型.yaml
topology_template:
  node_templates:
    my_node:
      type: MyNode
""", dict(repository=repository)).assert_success()


def test_import_single_long_form(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - file: {{ repository }}/imports/node-type.yaml
topology_template:
  node_templates:
    my_node:
      type: MyNode
""", dict(repository=repository)).assert_success()


@pytest.mark.skip(reason='not yet supported')
def test_import_single_repository(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
repositories:
  myrepository:
    url: {{ repository }}/imports/
imports:
  - file: node-type.yaml
    repository: myrepository
topology_template:
  node_templates:
    my_node:
      type: MyNode
""", dict(repository=repository)).assert_success()


@pytest.mark.skip(reason='not yet supported')
def test_import_single_namespace(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - file: {{ repository }}/imports/node-type.yaml
    namespace_uri:
    namespace_prefix: my_namespace
topology_template:
  node_templates:
    my_node:
      type: my_namespace.MyNode
""", dict(repository=repository)).assert_success()


# Failures

def test_import_not_found(parser):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - does_not_exist
""").assert_failure()


def test_import_bad(parser, repository):
    parser.parse_literal("""
tosca_definitions_version: tosca_simple_yaml_1_0
imports:
  - {{ repository }}/imports/bad.yaml
topology_template:
  node_templates:
    my_node:
      type: MyNode
""", dict(repository=repository)).assert_failure()
