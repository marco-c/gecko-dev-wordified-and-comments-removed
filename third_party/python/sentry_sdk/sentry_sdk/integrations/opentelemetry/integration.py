"
"
"
IMPORTANT
:
The
contents
of
this
file
are
part
of
a
proof
of
concept
and
as
such
are
experimental
and
not
suitable
for
production
use
.
They
may
be
changed
or
removed
at
any
time
without
prior
notice
.
"
"
"
import
sys
from
importlib
import
import_module
from
sentry_sdk
.
integrations
import
DidNotEnable
Integration
from
sentry_sdk
.
integrations
.
opentelemetry
.
span_processor
import
SentrySpanProcessor
from
sentry_sdk
.
integrations
.
opentelemetry
.
propagator
import
SentryPropagator
from
sentry_sdk
.
utils
import
logger
_get_installed_modules
from
sentry_sdk
.
_types
import
TYPE_CHECKING
try
:
    
from
opentelemetry
import
trace
    
from
opentelemetry
.
instrumentation
.
auto_instrumentation
.
_load
import
(
        
_load_distro
        
_load_instrumentors
    
)
    
from
opentelemetry
.
propagate
import
set_global_textmap
    
from
opentelemetry
.
sdk
.
trace
import
TracerProvider
except
ImportError
:
    
raise
DidNotEnable
(
"
opentelemetry
not
installed
"
)
if
TYPE_CHECKING
:
    
from
typing
import
Dict
CLASSES_TO_INSTRUMENT
=
{
    
"
fastapi
"
:
"
fastapi
.
FastAPI
"
    
"
flask
"
:
"
flask
.
Flask
"
}
class
OpenTelemetryIntegration
(
Integration
)
:
    
identifier
=
"
opentelemetry
"
    
staticmethod
    
def
setup_once
(
)
:
        
logger
.
warning
(
            
"
[
OTel
]
Initializing
highly
experimental
OpenTelemetry
support
.
"
            
"
Use
at
your
own
risk
.
"
        
)
        
original_classes
=
_record_unpatched_classes
(
)
        
try
:
            
distro
=
_load_distro
(
)
            
distro
.
configure
(
)
            
_load_instrumentors
(
distro
)
        
except
Exception
:
            
logger
.
exception
(
"
[
OTel
]
Failed
to
auto
-
initialize
OpenTelemetry
"
)
        
try
:
            
_patch_remaining_classes
(
original_classes
)
        
except
Exception
:
            
logger
.
exception
(
                
"
[
OTel
]
Failed
to
post
-
patch
instrumented
classes
.
"
                
"
You
might
have
to
make
sure
sentry_sdk
.
init
(
)
is
called
before
importing
anything
else
.
"
            
)
        
_setup_sentry_tracing
(
)
        
logger
.
debug
(
"
[
OTel
]
Finished
setting
up
OpenTelemetry
integration
"
)
def
_record_unpatched_classes
(
)
:
    
"
"
"
    
Keep
references
to
classes
that
are
about
to
be
instrumented
.
    
Used
to
search
for
unpatched
classes
after
the
instrumentation
has
run
so
    
that
they
can
be
patched
manually
.
    
"
"
"
    
installed_packages
=
_get_installed_modules
(
)
    
original_classes
=
{
}
    
for
package
orig_path
in
CLASSES_TO_INSTRUMENT
.
items
(
)
:
        
if
package
in
installed_packages
:
            
try
:
                
original_cls
=
_import_by_path
(
orig_path
)
            
except
(
AttributeError
ImportError
)
:
                
logger
.
debug
(
"
[
OTel
]
Failed
to
import
%
s
"
orig_path
)
                
continue
            
original_classes
[
package
]
=
original_cls
    
return
original_classes
def
_patch_remaining_classes
(
original_classes
)
:
    
"
"
"
    
Best
-
effort
attempt
to
patch
any
uninstrumented
classes
in
sys
.
modules
.
    
This
enables
us
to
not
care
about
the
order
of
imports
and
sentry_sdk
.
init
(
)
    
in
user
code
.
If
e
.
g
.
the
Flask
class
had
been
imported
before
sentry_sdk
    
was
init
(
)
ed
(
and
therefore
before
the
OTel
instrumentation
ran
)
it
would
    
not
be
instrumented
.
This
function
goes
over
remaining
uninstrumented
    
occurrences
of
the
class
in
sys
.
modules
and
replaces
them
with
the
    
instrumented
class
.
    
Since
this
is
looking
for
exact
matches
it
will
not
work
in
some
scenarios
    
(
e
.
g
.
if
someone
is
not
using
the
specific
class
explicitly
but
rather
    
inheriting
from
it
)
.
In
those
cases
it
'
s
still
necessary
to
sentry_sdk
.
init
(
)
    
before
importing
anything
that
'
s
supposed
to
be
instrumented
.
    
"
"
"
    
instrumented_classes
=
{
}
    
for
package
in
list
(
original_classes
.
keys
(
)
)
:
        
original_path
=
CLASSES_TO_INSTRUMENT
[
package
]
        
try
:
            
cls
=
_import_by_path
(
original_path
)
        
except
(
AttributeError
ImportError
)
:
            
logger
.
debug
(
                
"
[
OTel
]
Failed
to
check
if
class
has
been
instrumented
:
%
s
"
                
original_path
            
)
            
del
original_classes
[
package
]
            
continue
        
if
not
cls
.
__module__
.
startswith
(
"
opentelemetry
.
"
)
:
            
del
original_classes
[
package
]
            
continue
        
instrumented_classes
[
package
]
=
cls
    
if
not
instrumented_classes
:
        
return
    
for
module_name
module
in
sys
.
modules
.
copy
(
)
.
items
(
)
:
        
if
(
            
module_name
.
startswith
(
"
sentry_sdk
"
)
            
or
module_name
in
sys
.
builtin_module_names
        
)
:
            
continue
        
for
package
original_cls
in
original_classes
.
items
(
)
:
            
for
var_name
var
in
vars
(
module
)
.
copy
(
)
.
items
(
)
:
                
if
var
=
=
original_cls
:
                    
logger
.
debug
(
                        
"
[
OTel
]
Additionally
patching
%
s
from
%
s
"
                        
original_cls
                        
module_name
                    
)
                    
setattr
(
module
var_name
instrumented_classes
[
package
]
)
def
_import_by_path
(
path
)
:
    
parts
=
path
.
rsplit
(
"
.
"
maxsplit
=
1
)
    
return
getattr
(
import_module
(
parts
[
0
]
)
parts
[
-
1
]
)
def
_setup_sentry_tracing
(
)
:
    
provider
=
TracerProvider
(
)
    
provider
.
add_span_processor
(
SentrySpanProcessor
(
)
)
    
trace
.
set_tracer_provider
(
provider
)
    
set_global_textmap
(
SentryPropagator
(
)
)
