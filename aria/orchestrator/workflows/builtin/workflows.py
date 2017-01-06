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
A set of builtin workflows.
"""

from .utils import (create_node_instance_task, create_relationship_instance_task)
from ... import workflow


__all__ = (
    'install_node_instance',
    'uninstall_node_instance',
    'start_node_instance',
    'stop_node_instance',
)


@workflow(suffix_template='{node_instance.id}')
def install_node_instance(graph, node_instance, **kwargs):
    sequence = []

    # Create
    create_node_instance_task(
        'tosca.interfaces.node.lifecycle.Standard.create',
        node_instance, sequence)

    # Configure
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.pre_configure_source',
        'source_operations',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.pre_configure_target',
        'target_operations',
        node_instance, sequence)
    create_node_instance_task(
        'tosca.interfaces.node.lifecycle.Standard.configure',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.post_configure_source',
        'source_operations',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.post_configure_target',
        'target_operations',
        node_instance, sequence)

    # Start
    _create_start_tasks(sequence, node_instance)

    graph.sequence(*sequence)


@workflow(suffix_template='{node_instance.id}')
def uninstall_node_instance(graph, node_instance, **kwargs):
    sequence = []

    # Stop
    _create_stop_tasks(sequence, node_instance)

    # Delete
    create_node_instance_task(
        'tosca.interfaces.node.lifecycle.Standard.delete',
        node_instance, sequence)

    graph.sequence(*sequence)


@workflow(suffix_template='{node_instance.id}')
def start_node_instance(graph, node_instance, **kwargs):
    sequence = []
    _create_start_tasks(sequence, node_instance)
    graph.sequence(*sequence)


@workflow(suffix_template='{node_instance.id}')
def stop_node_instance(graph, node_instance, **kwargs):
    sequence = []
    _create_stop_tasks(sequence, node_instance)
    graph.sequence(*sequence)


def _create_start_tasks(sequence, node_instance):
    create_node_instance_task(
        'tosca.interfaces.node.lifecycle.Standard.start',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.add_source',
        'source_operations',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.add_target',
        'target_operations',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.target_changed',
        'target_operations',
        node_instance, sequence)


def _create_stop_tasks(sequence, node_instance):
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.remove_target',
        'target_operations',
        node_instance, sequence)
    create_relationship_instance_task(
        'tosca.interfaces.relationship.Configure.target_changed',
        'target_operations',
        node_instance, sequence)
    create_node_instance_task(
        'tosca.interfaces.node.lifecycle.Standard.stop',
        node_instance, sequence)
