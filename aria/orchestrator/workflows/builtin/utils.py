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

from ..api.task import OperationTask


def create_node_instance_task(operation_name, node_instance, sequence):
    if operation_name in node_instance.node.operations:
        sequence.append(
            OperationTask.node_instance(instance=node_instance,
                                        name=operation_name))


def create_relationship_instance_task(operation_name, operations_attr, node_instance, sequence):
    for relationship_instance in node_instance.outbound_relationship_instances:
        if operation_name in getattr(relationship_instance.relationship, operations_attr):
            sequence.append(
                OperationTask.relationship_instance(instance=relationship_instance,
                                                    name=operation_name,
                                                    operation_end=operations_attr))


def create_node_instance_task_dependencies(graph, node_instances, tasks, reverse=False):
    def get_task(node_instance_id):
        for index, node_instance in enumerate(node_instances):
            if node_instance.id == node_instance_id:
                return tasks[index]
        return None

    for index, node_instance in enumerate(node_instances):
        dependencies = []
        for relationship_instance in node_instance.outbound_relationship_instances:
            dependency = get_task(relationship_instance.target_node_instance.id)
            if dependency:
                dependencies.append(dependency)
        if dependencies:
            if reverse:
                for dependency in dependencies:
                    graph.add_dependency(dependency, tasks[index])
            else:
                graph.add_dependency(tasks[index], dependencies)


def create_node_instance_task_explicit(
        node_instance,
        operation,
        operation_kwargs,
        allow_kwargs_override):
    """
    A workflow which executes a single operation
    :param node_instance: the node instance to install
    :param basestring operation: the operation name
    :param dict operation_kwargs:
    :param bool allow_kwargs_override:
    :return:
    """

    if allow_kwargs_override is not None:
        operation_kwargs['allow_kwargs_override'] = allow_kwargs_override

    return OperationTask.node_instance(
        instance=node_instance,
        name=operation,
        inputs=operation_kwargs)
