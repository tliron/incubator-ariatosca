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

import platform

from sqlalchemy import (create_engine, orm) # @UnresolvedImport
from sqlalchemy.pool import StaticPool # @UnresolvedImport

from .. import (application_model_storage, application_resource_storage)
from ..orchestrator.workflows.api.task import OperationTask
from ..orchestrator.workflows.core.engine import Engine
from ..orchestrator.workflows.executor.thread import ThreadExecutor
from ..orchestrator import workflow
from ..orchestrator.context.workflow import WorkflowContext
from ..storage import model
from ..storage.sql_mapi import SQLAlchemyModelAPI
from ..storage.filesystem_rapi import FileSystemResourceAPI


SQLITE_MEMORY = 'sqlite:///:memory:'


class Workflow(object):
    """
    Executes a specific interface operation on all nodes or relationships
    in a deployment.
    """
    
    def __init__(self, deployment_id, initialize_model_storage_fn, operation):
        @workflow
        def cli_workflow(ctx, graph):
            for n in ctx.model.node_instance.iter():
                task = self.create_node_instance_task(n, operation)
                graph.add_tasks(task)

        workflow_context = self.create_workflow_context(deployment_id, initialize_model_storage_fn)
        tasks_graph = cli_workflow(ctx=workflow_context)
        self._engine = Engine(
            executor=ThreadExecutor(),
            workflow_context=workflow_context,
            tasks_graph=tasks_graph)
    
    def execute(self):
        self._engine.execute()
    
    def create_workflow_context(self, deployment_id, initialize_model_storage_fn):
        model_storage = self.create_sqlite_model_storage()
        initialize_model_storage_fn(model_storage)
        resource_storage = self.create_fs_resource_storage()
        return WorkflowContext(
            name='cli_workflow_context',
            model_storage=model_storage,
            resource_storage=resource_storage,
            deployment_id=deployment_id,
            workflow_name='cli_workflow',
            task_max_attempts=1,
            task_retry_interval=1)

    def create_node_instance_task(self, node_instance, operation):
        return OperationTask.node_instance(
            instance=node_instance,
            name=operation,
            inputs=None,
            max_attempts=None,
            retry_interval=None,
            ignore_failure=None)
                        
    def create_sqlite_model_storage(self, path=None):
        if path is not None:
            path_prefix = '' if 'Windows' in platform.system() else '/'
            sqlite_engine = create_engine(
                'sqlite:///%s%s' % (path_prefix, path))
        else:
            sqlite_engine = create_engine(
                SQLITE_MEMORY,
                connect_args={'check_same_thread': False},
                poolclass=StaticPool)
            
        model.DeclarativeBase.metadata.create_all(bind=sqlite_engine) # @UndefinedVariable
        sqlite_session_factory = orm.sessionmaker(bind=sqlite_engine)
        sqlite_session = orm.scoped_session(session_factory=sqlite_session_factory)
        sqlite_kwargs = dict(engine=sqlite_engine, session=sqlite_session)
        return application_model_storage(
            SQLAlchemyModelAPI,
            api_kwargs=sqlite_kwargs)
    
    def create_fs_resource_storage(self, directory='.'):
        fs_kwargs = dict(directory=directory)
        return application_resource_storage(
            FileSystemResourceAPI,
            api_kwargs=fs_kwargs)
