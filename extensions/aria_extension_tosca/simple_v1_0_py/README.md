
TOSCA.py
========

Premise
-------

TOSCA is a bad DSL because it's based on YAML. As such there are three things it does terribly:

First, YAML does not offer flow-control, such as "if" statements and "for" loops. This makes it
very hard to create configurable, dynamic service templates. There's only so much you can do with
service inputs and the "get_input" intrinsic function.

Second, YAML provides no access to external data sources. You can't pull in values from a database
or a RESTful service, and not even from environment variables.

For the above reasons, if you need to dynamically configure service templates, you would have to
generate your YAML file from a YAML generation, for example a template renderer like Jinja.
(ARIA does support Jinja templates).

Third, YAML offers no expression language and especially function calls, so it must explicitly
provide a limited number of "intrinsic function" implementations as well as constraint expressions
and a limited way to combine their return values via expressions.

A fourth limitation is that YAML is not designed for object-oriented languages like TOSCA, so
there's limited tooling support for designers: no IDE integration for TOSCA with code completion or
validation. These tools *can* be written, but do not exist yet.

The main advantage of YAML is that it is a platform-agnostic textual format, so that it can be read
easily by any TOSCA implementation.

Value Proposition
-----------------

However, we would like to suggest that a Python-based TOSCA DSL could be a better solution for
many use cases. Like YAML, Python is a textual format, but it inherently solves all the problems
mentioned above, and has mature tooling support in IDEs.

While it's not quite as platform-agnostic as YAML, there are Python implementations for all major
operating systems, even Java and .NET, making it possible to use TOSCA.py as a replacement for
the TOSCA parser of any TOSCA implementation. TOSCA.py can even be made to generate YAML as an
intermediary format. So it's still very portable.

Limitations
-----------

The only limitation for portability would be for the expression language: function calls rely
heavily on the internal modeling and API of the implementation, in this case being ARIA. So these
would not be portable. However, for some use cases the advantage of being restricted to ARIA might
outweigh the disadvantages. It would of course be possible to restrict usage in your TOSCA.py
templates to TOSCA-defined intrinsic functions only in to ensure portability. 
