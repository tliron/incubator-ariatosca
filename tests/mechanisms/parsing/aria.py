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

from __future__ import absolute_import  # so we can import root 'aria'

from aria.parser.loading import LiteralLocation
from aria.parser.consumption import (
    ConsumptionContext,
    ConsumerChain,
    Read,
    Validate,
    ServiceTemplate
)
from aria.utils.imports import import_fullname

from . import (Parser, Parsed)


class AriaParser(Parser):
    def _parse_literal(self, text):
        context = AriaParser.create_context()
        context.presentation.location = LiteralLocation(text)
        consumer = AriaParser.create_consumer(context)
        consumer.consume()
        parsed = Parsed()
        parsed.text = text
        for issue in context.validation.issues:
            parsed.issues.append(unicode(issue))
        return parsed

    @staticmethod
    def create_context(loader_source='aria.parser.loading.DefaultLoaderSource',
                       reader_source='aria.parser.reading.DefaultReaderSource',
                       presenter_source='aria.parser.presentation.DefaultPresenterSource',
                       presenter=None,
                       debug=False):
        context = ConsumptionContext()
        context.loading.loader_source = import_fullname(loader_source)()
        context.reading.reader_source = import_fullname(reader_source)()
        context.presentation.presenter_source = import_fullname(presenter_source)()
        context.presentation.presenter_class = import_fullname(presenter)
        context.presentation.threads = 1 # tests already run in maximum thread density
        context.presentation.print_exceptions = debug
        return context

    @staticmethod
    def create_consumer(context):
        return ConsumerChain(context, (
            Read,
            Validate,
            ServiceTemplate
        ))
