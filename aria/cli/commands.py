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
CLI various commands implementation
"""

import json
import os
import sys
import csv
import shutil
import tempfile
from glob import glob
from importlib import import_module
from datetime import datetime
from threading import RLock

from ruamel import yaml # @UnresolvedImport

from .. import extension
from ..logger import LoggerMixin
from ..orchestrator import operation
from ..parser import iter_specifications
from ..parser.consumption import (
    ConsumptionContext,
    ConsumerChain,
    Read,
    Validate,
    Model,
    Types,
    Inputs,
    Instance
)
from ..parser.loading import LiteralLocation, UriLocation
from ..storage import model
from ..utils.application import StorageManager
from ..utils.caching import cachedmethod
from ..utils.console import (puts, Colored, indent)
from ..utils.imports import (import_fullname, import_modules)
from .workflow import Workflow
from .exceptions import (
    AriaCliFormatInputsError,
    AriaCliYAMLInputsError,
    AriaCliInvalidInputsError
)
from . import csar


class BaseCommand(LoggerMixin):
    """
    Base class for CLI commands.
    """

    def __repr__(self):
        return 'AriaCli({cls.__name__})'.format(cls=self.__class__)

    def __call__(self, args_namespace, unknown_args):
        """
        __call__ method is called when running command
        :param args_namespace:
        """
        pass

    def parse_inputs(self, inputs):
        """
        Returns a dictionary of inputs `resources` can be:
        - A list of files.
        - A single file
        - A directory containing multiple input files
        - A key1=value1;key2=value2 pairs string.
        - Wildcard based string (e.g. *-inputs.yaml)
        """

        parsed_dict = {}

        def _format_to_dict(input_string):
            self.logger.info('Processing inputs source: {0}'.format(input_string))
            try:
                input_string = input_string.strip()
                try:
                    parsed_dict.update(json.loads(input_string))
                except BaseException:
                    parsed_dict.update((i.split('=')
                                        for i in input_string.split(';')
                                        if i))
            except Exception as exc:
                raise AriaCliFormatInputsError(str(exc), inputs=input_string)

        def _handle_inputs_source(input_path):
            self.logger.info('Processing inputs source: {0}'.format(input_path))
            try:
                with open(input_path) as input_file:
                    content = yaml.safe_load(input_file)
            except yaml.YAMLError as exc:
                raise AriaCliYAMLInputsError(
                    '"{0}" is not a valid YAML. {1}'.format(input_path, str(exc)))
            if isinstance(content, dict):
                parsed_dict.update(content)
                return
            if content is None:
                return
            raise AriaCliInvalidInputsError('Invalid inputs', inputs=input_path)

        for input_string in inputs if isinstance(inputs, list) else [inputs]:
            if os.path.isdir(input_string):
                for input_file in os.listdir(input_string):
                    _handle_inputs_source(os.path.join(input_string, input_file))
                continue
            input_files = glob(input_string)
            if input_files:
                for input_file in input_files:
                    _handle_inputs_source(input_file)
                continue
            _format_to_dict(input_string)
        return parsed_dict


class ParseCommand(BaseCommand):
    """
    :code:`parse` command.
    
    Given a blueprint, emits information in human-readable, JSON, or YAML format from various phases
    of the ARIA parser.
    """
    
    def __call__(self, args_namespace, unknown_args):
        super(ParseCommand, self).__call__(args_namespace, unknown_args)

        if args_namespace.prefix:
            for prefix in args_namespace.prefix:
                extension.parser.uri_loader_prefix().append(prefix)

        cachedmethod.ENABLED = args_namespace.cached_methods

        context = ParseCommand.create_context_from_namespace(args_namespace)
        context.args = unknown_args

        consumer = ConsumerChain(context, (Read, Validate))

        consumer_class_name = args_namespace.consumer
        dumper = None
        if consumer_class_name == 'presentation':
            dumper = consumer.consumers[0]
        elif consumer_class_name == 'model':
            consumer.append(Model)
        elif consumer_class_name == 'types':
            consumer.append(Model, Types)
        elif consumer_class_name == 'instance':
            consumer.append(Model, Inputs, Instance)
        else:
            consumer.append(Model, Inputs, Instance)
            consumer.append(import_fullname(consumer_class_name))

        if dumper is None:
            # Default to last consumer
            dumper = consumer.consumers[-1]

        consumer.consume()

        if not context.validation.dump_issues():
            dumper.dump()

    @staticmethod
    def create_context_from_namespace(namespace, **kwargs):
        args = vars(namespace).copy()
        args.update(kwargs)
        return ParseCommand.create_context(**args)

    @staticmethod
    def create_context(uri,
                       loader_source,
                       reader_source,
                       presenter_source,
                       presenter,
                       debug,
                       **kwargs):
        context = ConsumptionContext()
        context.loading.loader_source = import_fullname(loader_source)()
        context.reading.reader_source = import_fullname(reader_source)()
        context.presentation.location = UriLocation(uri) if isinstance(uri, basestring) else uri
        context.presentation.presenter_source = import_fullname(presenter_source)()
        context.presentation.presenter_class = import_fullname(presenter)
        context.presentation.print_exceptions = debug
        return context


terminal_lock = RLock()

@operation
def node_operation(ctx, **kwargs):
    with terminal_lock:
        print '> node instance: %s' % ctx.node_instance.name

@operation
def relationship_operation(ctx, **kwargs):
    with terminal_lock:
        print '> relationship instance: %s -> %s' % (
            ctx.relationship_instance.source_node_instance.name,
            ctx.relationship_instance.target_node_instance.name)


class WorkflowCommand(BaseCommand):
    """
    :code:`workflow` command.
    """
    
    def __call__(self, args_namespace, unknown_args):
        super(WorkflowCommand, self).__call__(args_namespace, unknown_args)

        # Parse
        context = ConsumptionContext()
        context.presentation.location = UriLocation(args_namespace.uri)
        consumer = ConsumerChain(context, (Read, Validate, Model, Inputs, Instance))
        consumer.consume()

        if context.validation.dump_issues():
            return
        
        # Put model in storage
        def initialize_model_storage(model_storage):
            blueprint = self.create_blueprint(context)
            model_storage.blueprint.put(blueprint)
            
            deployment = self.create_deployment(context, blueprint, args_namespace.deployment_id)
            model_storage.deployment.put(deployment)
            
            # Create nodes and node instances
            for node_template in context.modeling.model.node_templates.itervalues():
                n = self.create_node(deployment, node_template)
                model_storage.node.put(n)

                for node in context.modeling.instance.find_nodes(node_template.name):
                    ni = self.create_node_instance(n, node)
                    model_storage.node_instance.put(ni)
            
            # Create relationships
            for node_template in context.modeling.model.node_templates.itervalues():
                for index, requirement_template in enumerate(node_template.requirement_templates):
                    # We are currently limited only to requirements for specific node templates!
                    if requirement_template.target_node_template_name:
                        source = model_storage.node.get_by_name(node_template.name)
                        target = model_storage.node.get_by_name(
                            requirement_template.target_node_template_name)
                        r = self.create_relationship(source, target,
                                                     requirement_template.relationship_template)
                        model_storage.relationship.put(r)

                        for node in context.modeling.instance.find_nodes(node_template.name):
                            for relationship in node.relationships:
                                if relationship.source_requirement_index == index:
                                    source_instance = \
                                        model_storage.node_instance.get_by_name(node.id)
                                    target_instance = \
                                        model_storage.node_instance.get_by_name(
                                            relationship.target_node_id)
                                    ri = self.create_relationship_instance(r,
                                                                           source_instance,
                                                                           target_instance)
                                    model_storage.relationship_instance.put(ri)

        # Create workflow
        workflow = Workflow(
            args_namespace.deployment_id,
            initialize_model_storage,
            args_namespace.operation)
        
        # Execute
        workflow.execute()

    def create_blueprint(self, context):
        now = datetime.utcnow()
        main_file_name = unicode(context.presentation.location)
        try:
            name = context.modeling.model.metadata.values.get('template_name')
        except AttributeError:
            name = None
        return model.Blueprint(
            plan={},
            name=name or main_file_name,
            description=context.modeling.model.description or '',
            created_at=now,
            updated_at=now,
            main_file_name=main_file_name)
    
    def create_deployment(self, context, blueprint, id):
        now = datetime.utcnow()
        return model.Deployment(
            name='%s_%s' % (blueprint.name, id),
            blueprint_fk=blueprint.id,
            description=context.modeling.instance.description or '',
            created_at=now,
            updated_at=now,
            workflows={},
            inputs={},
            groups={},
            permalink='',
            policy_triggers={},
            policy_types={},
            outputs={},
            scaling_groups={})

    def create_node(self, deployment, node_template):
        operations = self.create_operations(node_template.interface_templates, 'node_operation')
        return model.Node(
            name=node_template.name,
            type=node_template.type_name,
            type_hierarchy=[],
            number_of_instances=node_template.default_instances,
            planned_number_of_instances=node_template.default_instances,
            deploy_number_of_instances=node_template.default_instances,
            properties={},
            operations=operations,
            min_number_of_instances=node_template.min_instances,
            max_number_of_instances=node_template.max_instances or 100,
            deployment_fk=deployment.id)

    def create_relationship(self, source, target, relationship_template):
        if relationship_template:
            source_operations = \
                self.create_operations(relationship_template.source_interface_templates,
                                       'relationship_operation')
            target_operations = \
                self.create_operations(relationship_template.target_interface_templates,
                                       'relationship_operation')
        else:
            source_operations = {}
            target_operations = {}
        return model.Relationship(
            source_node_fk=source.id,
            target_node_fk=target.id,
            source_interfaces={},
            source_operations=source_operations,
            target_interfaces={},
            target_operations=target_operations,
            type='rel_type',
            type_hierarchy=[],
            properties={})
    
    def create_node_instance(self, n, node):
        return model.NodeInstance(
            name=node.id,
            runtime_properties={},
            version=None,
            node_fk=n.id,
            state='',
            scaling_groups=[])

    def create_relationship_instance(self, relationship, source_instance, target_instance):
        return model.RelationshipInstance(
            relationship_fk=relationship.id,
            source_node_instance_fk=source_instance.id,
            target_node_instance_fk=target_instance.id)

    def create_operations(self, interfaces, fn_name):
        operations = {}
        for interface in interfaces.itervalues():
            operations[interface.type_name] = {} 
            for operation in interface.operation_templates.itervalues():
                n = '%s.%s' % (interface.type_name, operation.name)
                operations[n] = {'operation': '%s.%s' % (__name__, fn_name)}
        return operations
   

class InitCommand(BaseCommand):
    """
    :code:`init` command.
    
    Broken. Currently maintained for reference.
    """

    _IN_VIRTUAL_ENV = hasattr(sys, 'real_prefix')

    def __call__(self, args_namespace, unknown_args):
        super(InitCommand, self).__call__(args_namespace, unknown_args)
        self._workspace_setup()
        inputs = self.parse_inputs(args_namespace.input) if args_namespace.input else None
        plan, deployment_plan = self._parse_blueprint(args_namespace.blueprint_path, inputs)
        self._create_storage(
            blueprint_plan=plan,
            blueprint_path=args_namespace.blueprint_path,
            deployment_plan=deployment_plan,
            blueprint_id=args_namespace.blueprint_id,
            deployment_id=args_namespace.deployment_id,
            main_file_name=os.path.basename(args_namespace.blueprint_path))
        self.logger.info('Initiated {0}'.format(args_namespace.blueprint_path))
        self.logger.info(
            'If you make changes to the blueprint, '
            'run `aria local init -p {0}` command again to apply them'.format(
                args_namespace.blueprint_path))

    def _workspace_setup(self):
        try:
            create_user_space()
            self.logger.debug(
                'created user space path in: {0}'.format(user_space()))
        except IOError:
            self.logger.debug(
                'user space path already exist - {0}'.format(user_space()))
        try:
            create_local_storage()
            self.logger.debug(
                'created local storage path in: {0}'.format(local_storage()))
        except IOError:
            self.logger.debug(
                'local storage path already exist - {0}'.format(local_storage()))
        return local_storage()

    def _parse_blueprint(self, blueprint_path, inputs=None):
        # TODO
        pass

    @staticmethod
    def _create_storage(
            blueprint_path,
            blueprint_plan,
            deployment_plan,
            blueprint_id,
            deployment_id,
            main_file_name=None):
        resource_storage = application_resource_storage(
            FileSystemResourceDriver(local_resource_storage()))
        model_storage = application_model_storage(
            FileSystemModelDriver(local_model_storage()))
        resource_storage.setup()
        model_storage.setup()
        storage_manager = StorageManager(
            model_storage=model_storage,
            resource_storage=resource_storage,
            blueprint_path=blueprint_path,
            blueprint_id=blueprint_id,
            blueprint_plan=blueprint_plan,
            deployment_id=deployment_id,
            deployment_plan=deployment_plan
        )
        storage_manager.create_blueprint_storage(
            blueprint_path,
            main_file_name=main_file_name
        )
        storage_manager.create_nodes_storage()
        storage_manager.create_deployment_storage()
        storage_manager.create_node_instances_storage()


class ExecuteCommand(BaseCommand):
    """
    :code:`execute` command.

    Broken. Currently maintained for reference.
    """

    def __call__(self, args_namespace, unknown_args):
        super(ExecuteCommand, self).__call__(args_namespace, unknown_args)
        parameters = (self.parse_inputs(args_namespace.parameters)
                      if args_namespace.parameters else {})
        resource_storage = application_resource_storage(
            FileSystemResourceDriver(local_resource_storage()))
        model_storage = application_model_storage(
            FileSystemModelDriver(local_model_storage()))
        deployment = model_storage.deployment.get(args_namespace.deployment_id)

        try:
            workflow = deployment.workflows[args_namespace.workflow_id]
        except KeyError:
            raise ValueError(
                '{0} workflow does not exist. existing workflows are: {1}'.format(
                    args_namespace.workflow_id,
                    deployment.workflows.keys()))

        workflow_parameters = self._merge_and_validate_execution_parameters(
            workflow,
            args_namespace.workflow_id,
            parameters
        )
        workflow_context = WorkflowContext(
            name=args_namespace.workflow_id,
            model_storage=model_storage,
            resource_storage=resource_storage,
            deployment_id=args_namespace.deployment_id,
            workflow_id=args_namespace.workflow_id,
            parameters=workflow_parameters,
        )
        workflow_function = self._load_workflow_handler(workflow['operation'])
        tasks_graph = workflow_function(workflow_context, **workflow_context.parameters)
        executor = ProcessExecutor()
        workflow_engine = Engine(executor=executor,
                                 workflow_context=workflow_context,
                                 tasks_graph=tasks_graph)
        workflow_engine.execute()
        executor.close()

    @staticmethod
    def _merge_and_validate_execution_parameters(
            workflow,
            workflow_name,
            execution_parameters):
        merged_parameters = {}
        workflow_parameters = workflow.get('parameters', {})
        missing_mandatory_parameters = set()

        for name, param in workflow_parameters.iteritems():
            if 'default' not in param:
                if name not in execution_parameters:
                    missing_mandatory_parameters.add(name)
                    continue
                merged_parameters[name] = execution_parameters[name]
                continue
            merged_parameters[name] = (execution_parameters[name] if name in execution_parameters
                                       else param['default'])

        if missing_mandatory_parameters:
            raise ValueError(
                'Workflow "{0}" must be provided with the following '
                'parameters to execute: {1}'.format(
                    workflow_name, ','.join(missing_mandatory_parameters)))

        custom_parameters = dict(
            (k, v) for (k, v) in execution_parameters.iteritems()
            if k not in workflow_parameters)

        if custom_parameters:
            raise ValueError(
                'Workflow "{0}" does not have the following parameters declared: {1}. '
                'Remove these parameters'.format(
                    workflow_name, ','.join(custom_parameters.keys())))

        return merged_parameters

    @staticmethod
    def _load_workflow_handler(handler_path):
        module_name, spec_handler_name = handler_path.rsplit('.', 1)
        try:
            module = import_module(module_name)
            return getattr(module, spec_handler_name)
        except ImportError:
            # TODO: exception handler
            raise
        except AttributeError:
            # TODO: exception handler
            raise


class BaseCSARCommand(BaseCommand):
    @staticmethod
    def _parse_and_dump(reader):
        context = ConsumptionContext()
        context.loading.prefixes += [os.path.join(reader.destination, 'definitions')]
        context.presentation.location = LiteralLocation(reader.entry_definitions_yaml)
        chain = ConsumerChain(context, (Read, Validate, Model, Instance))
        chain.consume()
        if context.validation.dump_issues():
            raise RuntimeError('Validation failed')
        dumper = chain.consumers[-1]
        dumper.dump()

    def _read(self, source, destination):
        reader = csar.read(
            source=source,
            destination=destination,
            logger=self.logger)
        self.logger.info(
            'Path: {r.destination}\n'
            'TOSCA meta file version: {r.meta_file_version}\n'
            'CSAR Version: {r.csar_version}\n'
            'Created By: {r.created_by}\n'
            'Entry definitions: {r.entry_definitions}'
            .format(r=reader))
        self._parse_and_dump(reader)

    def _validate(self, source):
        workdir = tempfile.mkdtemp()
        try:
            self._read(
                source=source,
                destination=workdir)
        finally:
            shutil.rmtree(workdir, ignore_errors=True)


class CSARCreateCommand(BaseCSARCommand):
    def __call__(self, args_namespace, unknown_args):
        super(CSARCreateCommand, self).__call__(args_namespace, unknown_args)
        csar.write(
            source=args_namespace.source,
            entry=args_namespace.entry,
            destination=args_namespace.destination,
            logger=self.logger)
        self._validate(args_namespace.destination)


class CSAROpenCommand(BaseCSARCommand):
    def __call__(self, args_namespace, unknown_args):
        super(CSAROpenCommand, self).__call__(args_namespace, unknown_args)
        self._read(
            source=args_namespace.source,
            destination=args_namespace.destination)


class CSARValidateCommand(BaseCSARCommand):
    def __call__(self, args_namespace, unknown_args):
        super(CSARValidateCommand, self).__call__(args_namespace, unknown_args)
        self._validate(args_namespace.source)


class SpecCommand(BaseCommand):
    """
    :code:`spec` command.
    
    Emits all uses of :code:`@dsl_specification` in the codebase, in human-readable or CSV format.
    """
    
    def __call__(self, args_namespace, unknown_args):
        super(SpecCommand, self).__call__(args_namespace, unknown_args)

        # Make sure that all @dsl_specification decorators are processed
        for pkg in extension.parser.specification_package():
            import_modules(pkg)

        # TODO: scan YAML documents as well

        if args_namespace.csv:
            writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
            writer.writerow(('Specification', 'Section', 'Code', 'URL'))
            for spec, sections in iter_specifications():
                for section, details in sections:
                    writer.writerow((spec, section, details['code'], details['url']))

        else:
            for spec, sections in iter_specifications():
                puts(Colored.cyan(spec))
                with indent(2):
                    for section, details in sections:
                        puts(Colored.blue(section))
                        with indent(2):
                            for k, v in details.iteritems():
                                puts('%s: %s' % (Colored.magenta(k), v))
