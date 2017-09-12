
TOSCA.py
========

Premise
-------

TOSCA is a bad DSL because it's based on YAML. As such there are three things it does terribly:

First, YAML is not offers no flow-control, such as "if" statements and "for" loops.

Second, YAML provides no access to external data sources. You can't pull in values from a database
or a RESTful service, and not even from environment variables.

For the above reasons, if you need to dynamically configure service templates, you would have to
generate your YAML file from a YAML generation, for example a template renderer like Jinja.

Third, it offers no expression language and especially function calls, so it must explicitly provide
a limited number of "intrinsic function" implementations and a limited way to combine their return
values via expressions.

A fourth limitation is that YAML is not designed for object-oriented language likes TOSCA, so
there's limited tooling support for designers: no IDE integration for TOSCA with code completion or
validation. These tools can be written, but none exists yet.

The main advantage of YAML is that it is a platform-agnostic textual format, so that it can be read
easily by any TOSCA implementation.

However, we would like to suggest that a Python-based TOSCA DSL could be a better solution for
many use cases. Like YAML, Python is a textual format, but it inherently solves all the problems
mentioned above, and has mature tooling support in IDEs.

While it's not quite as platform-agnostic as YAML, there are Python implementations for all major
operating systems, even Java and .NET, making it possible to use TOSCA.py as a replacement for
the TOSCA parser of any TOSCA implementation. TOSCA.py can even be made to generate YAML as an
intermediary format.

The only possible limitation would be for the expression language: function calls rely heavily on
the internal modeling and API of the implementation, in this case being ARIA. So these would not
be portable. However, for some use cases the advantage of being restricted to ARIA might outweigh
the disadvantages. It would of course be possible to restrict usage to TOSCA-defined intrinsic
functions to ensure portability. 
