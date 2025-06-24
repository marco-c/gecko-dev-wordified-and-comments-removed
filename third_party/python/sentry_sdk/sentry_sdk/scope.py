import
os
import
sys
import
warnings
from
copy
import
copy
deepcopy
from
collections
import
deque
from
contextlib
import
contextmanager
from
enum
import
Enum
from
datetime
import
datetime
timezone
from
functools
import
wraps
from
itertools
import
chain
from
sentry_sdk
.
_types
import
AnnotatedValue
from
sentry_sdk
.
attachments
import
Attachment
from
sentry_sdk
.
consts
import
DEFAULT_MAX_BREADCRUMBS
FALSE_VALUES
INSTRUMENTER
from
sentry_sdk
.
feature_flags
import
FlagBuffer
DEFAULT_FLAG_CAPACITY
from
sentry_sdk
.
profiler
.
continuous_profiler
import
(
    
get_profiler_id
    
try_autostart_continuous_profiler
    
try_profile_lifecycle_trace_start
)
from
sentry_sdk
.
profiler
.
transaction_profiler
import
Profile
from
sentry_sdk
.
session
import
Session
from
sentry_sdk
.
tracing_utils
import
(
    
Baggage
    
has_tracing_enabled
    
normalize_incoming_data
    
PropagationContext
)
from
sentry_sdk
.
tracing
import
(
    
BAGGAGE_HEADER_NAME
    
SENTRY_TRACE_HEADER_NAME
    
NoOpSpan
    
Span
    
Transaction
)
from
sentry_sdk
.
utils
import
(
    
capture_internal_exception
    
capture_internal_exceptions
    
ContextVar
    
datetime_from_isoformat
    
disable_capture_event
    
event_from_exception
    
exc_info_from_error
    
logger
)
import
typing
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
collections
.
abc
import
Mapping
MutableMapping
    
from
typing
import
Any
    
from
typing
import
Callable
    
from
typing
import
Deque
    
from
typing
import
Dict
    
from
typing
import
Generator
    
from
typing
import
Iterator
    
from
typing
import
List
    
from
typing
import
Optional
    
from
typing
import
ParamSpec
    
from
typing
import
Tuple
    
from
typing
import
TypeVar
    
from
typing
import
Union
    
from
typing_extensions
import
Unpack
    
from
sentry_sdk
.
_types
import
(
        
Breadcrumb
        
BreadcrumbHint
        
ErrorProcessor
        
Event
        
EventProcessor
        
ExcInfo
        
Hint
        
LogLevelStr
        
SamplingContext
        
Type
    
)
    
from
sentry_sdk
.
tracing
import
TransactionKwargs
    
import
sentry_sdk
    
P
=
ParamSpec
(
"
P
"
)
    
R
=
TypeVar
(
"
R
"
)
    
F
=
TypeVar
(
"
F
"
bound
=
Callable
[
.
.
.
Any
]
)
    
T
=
TypeVar
(
"
T
"
)
_global_scope
=
None
_isolation_scope
=
ContextVar
(
"
isolation_scope
"
default
=
None
)
_current_scope
=
ContextVar
(
"
current_scope
"
default
=
None
)
global_event_processors
=
[
]
class
ScopeType
(
Enum
)
:
    
CURRENT
=
"
current
"
    
ISOLATION
=
"
isolation
"
    
GLOBAL
=
"
global
"
    
MERGED
=
"
merged
"
class
_ScopeManager
:
    
def
__init__
(
self
hub
=
None
)
:
        
self
.
_old_scopes
=
[
]
    
def
__enter__
(
self
)
:
        
isolation_scope
=
Scope
.
get_isolation_scope
(
)
        
self
.
_old_scopes
.
append
(
isolation_scope
)
        
forked_scope
=
isolation_scope
.
fork
(
)
        
_isolation_scope
.
set
(
forked_scope
)
        
return
forked_scope
    
def
__exit__
(
self
exc_type
exc_value
tb
)
:
        
old_scope
=
self
.
_old_scopes
.
pop
(
)
        
_isolation_scope
.
set
(
old_scope
)
def
add_global_event_processor
(
processor
)
:
    
global_event_processors
.
append
(
processor
)
def
_attr_setter
(
fn
)
:
    
return
property
(
fset
=
fn
doc
=
fn
.
__doc__
)
def
_disable_capture
(
fn
)
:
    
wraps
(
fn
)
    
def
wrapper
(
self
*
args
*
*
kwargs
)
:
        
if
not
self
.
_should_capture
:
            
return
        
try
:
            
self
.
_should_capture
=
False
            
return
fn
(
self
*
args
*
*
kwargs
)
        
finally
:
            
self
.
_should_capture
=
True
    
return
wrapper
class
Scope
:
    
"
"
"
The
scope
holds
extra
information
that
should
be
sent
with
all
    
events
that
belong
to
it
.
    
"
"
"
    
__slots__
=
(
        
"
_level
"
        
"
_name
"
        
"
_fingerprint
"
        
"
_transaction
"
        
"
_transaction_info
"
        
"
_user
"
        
"
_tags
"
        
"
_contexts
"
        
"
_extras
"
        
"
_breadcrumbs
"
        
"
_n_breadcrumbs_truncated
"
        
"
_event_processors
"
        
"
_error_processors
"
        
"
_should_capture
"
        
"
_span
"
        
"
_session
"
        
"
_attachments
"
        
"
_force_auto_session_tracking
"
        
"
_profile
"
        
"
_propagation_context
"
        
"
client
"
        
"
_type
"
        
"
_last_event_id
"
        
"
_flags
"
    
)
    
def
__init__
(
self
ty
=
None
client
=
None
)
:
        
self
.
_type
=
ty
        
self
.
_event_processors
=
[
]
        
self
.
_error_processors
=
[
]
        
self
.
_name
=
None
        
self
.
_propagation_context
=
None
        
self
.
_n_breadcrumbs_truncated
=
0
        
self
.
client
=
NonRecordingClient
(
)
        
if
client
is
not
None
:
            
self
.
set_client
(
client
)
        
self
.
clear
(
)
        
incoming_trace_information
=
self
.
_load_trace_data_from_env
(
)
        
self
.
generate_propagation_context
(
incoming_data
=
incoming_trace_information
)
    
def
__copy__
(
self
)
:
        
"
"
"
        
Returns
a
copy
of
this
scope
.
        
This
also
creates
a
copy
of
all
referenced
data
structures
.
        
"
"
"
        
rv
=
object
.
__new__
(
self
.
__class__
)
        
rv
.
_type
=
self
.
_type
        
rv
.
client
=
self
.
client
        
rv
.
_level
=
self
.
_level
        
rv
.
_name
=
self
.
_name
        
rv
.
_fingerprint
=
self
.
_fingerprint
        
rv
.
_transaction
=
self
.
_transaction
        
rv
.
_transaction_info
=
dict
(
self
.
_transaction_info
)
        
rv
.
_user
=
self
.
_user
        
rv
.
_tags
=
dict
(
self
.
_tags
)
        
rv
.
_contexts
=
dict
(
self
.
_contexts
)
        
rv
.
_extras
=
dict
(
self
.
_extras
)
        
rv
.
_breadcrumbs
=
copy
(
self
.
_breadcrumbs
)
        
rv
.
_n_breadcrumbs_truncated
=
copy
(
self
.
_n_breadcrumbs_truncated
)
        
rv
.
_event_processors
=
list
(
self
.
_event_processors
)
        
rv
.
_error_processors
=
list
(
self
.
_error_processors
)
        
rv
.
_propagation_context
=
self
.
_propagation_context
        
rv
.
_should_capture
=
self
.
_should_capture
        
rv
.
_span
=
self
.
_span
        
rv
.
_session
=
self
.
_session
        
rv
.
_force_auto_session_tracking
=
self
.
_force_auto_session_tracking
        
rv
.
_attachments
=
list
(
self
.
_attachments
)
        
rv
.
_profile
=
self
.
_profile
        
rv
.
_last_event_id
=
self
.
_last_event_id
        
rv
.
_flags
=
deepcopy
(
self
.
_flags
)
        
return
rv
    
classmethod
    
def
get_current_scope
(
cls
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Returns
the
current
scope
.
        
"
"
"
        
current_scope
=
_current_scope
.
get
(
)
        
if
current_scope
is
None
:
            
current_scope
=
Scope
(
ty
=
ScopeType
.
CURRENT
)
            
_current_scope
.
set
(
current_scope
)
        
return
current_scope
    
classmethod
    
def
set_current_scope
(
cls
new_current_scope
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Sets
the
given
scope
as
the
new
current
scope
overwriting
the
existing
current
scope
.
        
:
param
new_current_scope
:
The
scope
to
set
as
the
new
current
scope
.
        
"
"
"
        
_current_scope
.
set
(
new_current_scope
)
    
classmethod
    
def
get_isolation_scope
(
cls
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Returns
the
isolation
scope
.
        
"
"
"
        
isolation_scope
=
_isolation_scope
.
get
(
)
        
if
isolation_scope
is
None
:
            
isolation_scope
=
Scope
(
ty
=
ScopeType
.
ISOLATION
)
            
_isolation_scope
.
set
(
isolation_scope
)
        
return
isolation_scope
    
classmethod
    
def
set_isolation_scope
(
cls
new_isolation_scope
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Sets
the
given
scope
as
the
new
isolation
scope
overwriting
the
existing
isolation
scope
.
        
:
param
new_isolation_scope
:
The
scope
to
set
as
the
new
isolation
scope
.
        
"
"
"
        
_isolation_scope
.
set
(
new_isolation_scope
)
    
classmethod
    
def
get_global_scope
(
cls
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Returns
the
global
scope
.
        
"
"
"
        
global
_global_scope
        
if
_global_scope
is
None
:
            
_global_scope
=
Scope
(
ty
=
ScopeType
.
GLOBAL
)
        
return
_global_scope
    
classmethod
    
def
last_event_id
(
cls
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
2
.
0
        
Returns
event
ID
of
the
event
most
recently
captured
by
the
isolation
scope
or
None
if
no
event
        
has
been
captured
.
We
do
not
consider
events
that
are
dropped
e
.
g
.
by
a
before_send
hook
.
        
Transactions
also
are
not
considered
events
in
this
context
.
        
The
event
corresponding
to
the
returned
event
ID
is
NOT
guaranteed
to
actually
be
sent
to
Sentry
;
        
whether
the
event
is
sent
depends
on
the
transport
.
The
event
could
be
sent
later
or
not
at
all
.
        
Even
a
sent
event
could
fail
to
arrive
in
Sentry
due
to
network
issues
exhausted
quotas
or
        
various
other
reasons
.
        
"
"
"
        
return
cls
.
get_isolation_scope
(
)
.
_last_event_id
    
def
_merge_scopes
(
self
additional_scope
=
None
additional_scope_kwargs
=
None
)
:
        
"
"
"
        
Merges
global
isolation
and
current
scope
into
a
new
scope
and
        
adds
the
given
additional
scope
or
additional
scope
kwargs
to
it
.
        
"
"
"
        
if
additional_scope
and
additional_scope_kwargs
:
            
raise
TypeError
(
"
cannot
provide
scope
and
kwargs
"
)
        
final_scope
=
copy
(
_global_scope
)
if
_global_scope
is
not
None
else
Scope
(
)
        
final_scope
.
_type
=
ScopeType
.
MERGED
        
isolation_scope
=
_isolation_scope
.
get
(
)
        
if
isolation_scope
is
not
None
:
            
final_scope
.
update_from_scope
(
isolation_scope
)
        
current_scope
=
_current_scope
.
get
(
)
        
if
current_scope
is
not
None
:
            
final_scope
.
update_from_scope
(
current_scope
)
        
if
self
!
=
current_scope
and
self
!
=
isolation_scope
:
            
final_scope
.
update_from_scope
(
self
)
        
if
additional_scope
is
not
None
:
            
if
callable
(
additional_scope
)
:
                
additional_scope
(
final_scope
)
            
else
:
                
final_scope
.
update_from_scope
(
additional_scope
)
        
elif
additional_scope_kwargs
:
            
final_scope
.
update_from_kwargs
(
*
*
additional_scope_kwargs
)
        
return
final_scope
    
classmethod
    
def
get_client
(
cls
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Returns
the
currently
used
:
py
:
class
:
sentry_sdk
.
Client
.
        
This
checks
the
current
scope
the
isolation
scope
and
the
global
scope
for
a
client
.
        
If
no
client
is
available
a
:
py
:
class
:
sentry_sdk
.
client
.
NonRecordingClient
is
returned
.
        
"
"
"
        
current_scope
=
_current_scope
.
get
(
)
        
try
:
            
client
=
current_scope
.
client
        
except
AttributeError
:
            
client
=
None
        
if
client
is
not
None
and
client
.
is_active
(
)
:
            
return
client
        
isolation_scope
=
_isolation_scope
.
get
(
)
        
try
:
            
client
=
isolation_scope
.
client
        
except
AttributeError
:
            
client
=
None
        
if
client
is
not
None
and
client
.
is_active
(
)
:
            
return
client
        
try
:
            
client
=
_global_scope
.
client
        
except
AttributeError
:
            
client
=
None
        
if
client
is
not
None
and
client
.
is_active
(
)
:
            
return
client
        
return
NonRecordingClient
(
)
    
def
set_client
(
self
client
=
None
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Sets
the
client
for
this
scope
.
        
:
param
client
:
The
client
to
use
in
this
scope
.
            
If
None
the
client
of
the
scope
will
be
replaced
by
a
:
py
:
class
:
sentry_sdk
.
NonRecordingClient
.
        
"
"
"
        
self
.
client
=
client
if
client
is
not
None
else
NonRecordingClient
(
)
    
def
fork
(
self
)
:
        
"
"
"
        
.
.
versionadded
:
:
2
.
0
.
0
        
Returns
a
fork
of
this
scope
.
        
"
"
"
        
forked_scope
=
copy
(
self
)
        
return
forked_scope
    
def
_load_trace_data_from_env
(
self
)
:
        
"
"
"
        
Load
Sentry
trace
id
and
baggage
from
environment
variables
.
        
Can
be
disabled
by
setting
SENTRY_USE_ENVIRONMENT
to
"
false
"
.
        
"
"
"
        
incoming_trace_information
=
None
        
sentry_use_environment
=
(
            
os
.
environ
.
get
(
"
SENTRY_USE_ENVIRONMENT
"
)
or
"
"
        
)
.
lower
(
)
        
use_environment
=
sentry_use_environment
not
in
FALSE_VALUES
        
if
use_environment
:
            
incoming_trace_information
=
{
}
            
if
os
.
environ
.
get
(
"
SENTRY_TRACE
"
)
:
                
incoming_trace_information
[
SENTRY_TRACE_HEADER_NAME
]
=
(
                    
os
.
environ
.
get
(
"
SENTRY_TRACE
"
)
or
"
"
                
)
            
if
os
.
environ
.
get
(
"
SENTRY_BAGGAGE
"
)
:
                
incoming_trace_information
[
BAGGAGE_HEADER_NAME
]
=
(
                    
os
.
environ
.
get
(
"
SENTRY_BAGGAGE
"
)
or
"
"
                
)
        
return
incoming_trace_information
or
None
    
def
set_new_propagation_context
(
self
)
:
        
"
"
"
        
Creates
a
new
propagation
context
and
sets
it
as
_propagation_context
.
Overwriting
existing
one
.
        
"
"
"
        
self
.
_propagation_context
=
PropagationContext
(
)
    
def
generate_propagation_context
(
self
incoming_data
=
None
)
:
        
"
"
"
        
Makes
sure
the
propagation
context
is
set
on
the
scope
.
        
If
there
is
incoming_data
overwrite
existing
propagation
context
.
        
If
there
is
no
incoming_data
create
new
propagation
context
but
do
NOT
overwrite
if
already
existing
.
        
"
"
"
        
if
incoming_data
:
            
propagation_context
=
PropagationContext
.
from_incoming_data
(
incoming_data
)
            
if
propagation_context
is
not
None
:
                
self
.
_propagation_context
=
propagation_context
        
if
self
.
_type
!
=
ScopeType
.
CURRENT
:
            
if
self
.
_propagation_context
is
None
:
                
self
.
set_new_propagation_context
(
)
    
def
get_dynamic_sampling_context
(
self
)
:
        
"
"
"
        
Returns
the
Dynamic
Sampling
Context
from
the
Propagation
Context
.
        
If
not
existing
creates
a
new
one
.
        
"
"
"
        
if
self
.
_propagation_context
is
None
:
            
return
None
        
baggage
=
self
.
get_baggage
(
)
        
if
baggage
is
not
None
:
            
self
.
_propagation_context
.
dynamic_sampling_context
=
(
                
baggage
.
dynamic_sampling_context
(
)
            
)
        
return
self
.
_propagation_context
.
dynamic_sampling_context
    
def
get_traceparent
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
        
Returns
the
Sentry
"
sentry
-
trace
"
header
(
aka
the
traceparent
)
from
the
        
currently
active
span
or
the
scopes
Propagation
Context
.
        
"
"
"
        
client
=
self
.
get_client
(
)
        
if
has_tracing_enabled
(
client
.
options
)
and
self
.
span
is
not
None
:
            
return
self
.
span
.
to_traceparent
(
)
        
if
self
.
_propagation_context
is
not
None
:
            
traceparent
=
"
%
s
-
%
s
"
%
(
                
self
.
_propagation_context
.
trace_id
                
self
.
_propagation_context
.
span_id
            
)
            
return
traceparent
        
return
self
.
get_isolation_scope
(
)
.
get_traceparent
(
)
    
def
get_baggage
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
        
Returns
the
Sentry
"
baggage
"
header
containing
trace
information
from
the
        
currently
active
span
or
the
scopes
Propagation
Context
.
        
"
"
"
        
client
=
self
.
get_client
(
)
        
if
has_tracing_enabled
(
client
.
options
)
and
self
.
span
is
not
None
:
            
return
self
.
span
.
to_baggage
(
)
        
if
self
.
_propagation_context
is
not
None
:
            
dynamic_sampling_context
=
(
                
self
.
_propagation_context
.
dynamic_sampling_context
            
)
            
if
dynamic_sampling_context
is
None
:
                
return
Baggage
.
from_options
(
self
)
            
else
:
                
return
Baggage
(
dynamic_sampling_context
)
        
return
self
.
get_isolation_scope
(
)
.
get_baggage
(
)
    
def
get_trace_context
(
self
)
:
        
"
"
"
        
Returns
the
Sentry
"
trace
"
context
from
the
Propagation
Context
.
        
"
"
"
        
if
self
.
_propagation_context
is
None
:
            
return
None
        
trace_context
=
{
            
"
trace_id
"
:
self
.
_propagation_context
.
trace_id
            
"
span_id
"
:
self
.
_propagation_context
.
span_id
            
"
parent_span_id
"
:
self
.
_propagation_context
.
parent_span_id
            
"
dynamic_sampling_context
"
:
self
.
get_dynamic_sampling_context
(
)
        
}
        
return
trace_context
    
def
trace_propagation_meta
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
        
Return
meta
tags
which
should
be
injected
into
HTML
templates
        
to
allow
propagation
of
trace
information
.
        
"
"
"
        
span
=
kwargs
.
pop
(
"
span
"
None
)
        
if
span
is
not
None
:
            
logger
.
warning
(
                
"
The
parameter
span
in
trace_propagation_meta
(
)
is
deprecated
and
will
be
removed
in
the
future
.
"
            
)
        
meta
=
"
"
        
sentry_trace
=
self
.
get_traceparent
(
)
        
if
sentry_trace
is
not
None
:
            
meta
+
=
'
<
meta
name
=
"
%
s
"
content
=
"
%
s
"
>
'
%
(
                
SENTRY_TRACE_HEADER_NAME
                
sentry_trace
            
)
        
baggage
=
self
.
get_baggage
(
)
        
if
baggage
is
not
None
:
            
meta
+
=
'
<
meta
name
=
"
%
s
"
content
=
"
%
s
"
>
'
%
(
                
BAGGAGE_HEADER_NAME
                
baggage
.
serialize
(
)
            
)
        
return
meta
    
def
iter_headers
(
self
)
:
        
"
"
"
        
Creates
a
generator
which
returns
the
sentry
-
trace
and
baggage
headers
from
the
Propagation
Context
.
        
"
"
"
        
if
self
.
_propagation_context
is
not
None
:
            
traceparent
=
self
.
get_traceparent
(
)
            
if
traceparent
is
not
None
:
                
yield
SENTRY_TRACE_HEADER_NAME
traceparent
            
dsc
=
self
.
get_dynamic_sampling_context
(
)
            
if
dsc
is
not
None
:
                
baggage
=
Baggage
(
dsc
)
.
serialize
(
)
                
yield
BAGGAGE_HEADER_NAME
baggage
    
def
iter_trace_propagation_headers
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
        
Return
HTTP
headers
which
allow
propagation
of
trace
data
.
        
If
a
span
is
given
the
trace
data
will
taken
from
the
span
.
        
If
no
span
is
given
the
trace
data
is
taken
from
the
scope
.
        
"
"
"
        
client
=
self
.
get_client
(
)
        
if
not
client
.
options
.
get
(
"
propagate_traces
"
)
:
            
warnings
.
warn
(
                
"
The
propagate_traces
parameter
is
deprecated
.
Please
use
trace_propagation_targets
instead
.
"
                
DeprecationWarning
                
stacklevel
=
2
            
)
            
return
        
span
=
kwargs
.
pop
(
"
span
"
None
)
        
span
=
span
or
self
.
span
        
if
has_tracing_enabled
(
client
.
options
)
and
span
is
not
None
:
            
for
header
in
span
.
iter_headers
(
)
:
                
yield
header
        
else
:
            
if
self
.
_propagation_context
is
not
None
:
                
for
header
in
self
.
iter_headers
(
)
:
                    
yield
header
            
else
:
                
current_scope
=
self
.
get_current_scope
(
)
                
if
current_scope
.
_propagation_context
is
not
None
:
                    
for
header
in
current_scope
.
iter_headers
(
)
:
                        
yield
header
                
else
:
                    
isolation_scope
=
self
.
get_isolation_scope
(
)
                    
if
isolation_scope
.
_propagation_context
is
not
None
:
                        
for
header
in
isolation_scope
.
iter_headers
(
)
:
                            
yield
header
    
def
get_active_propagation_context
(
self
)
:
        
if
self
.
_propagation_context
is
not
None
:
            
return
self
.
_propagation_context
        
current_scope
=
self
.
get_current_scope
(
)
        
if
current_scope
.
_propagation_context
is
not
None
:
            
return
current_scope
.
_propagation_context
        
isolation_scope
=
self
.
get_isolation_scope
(
)
        
if
isolation_scope
.
_propagation_context
is
not
None
:
            
return
isolation_scope
.
_propagation_context
        
return
None
    
def
clear
(
self
)
:
        
"
"
"
Clears
the
entire
scope
.
"
"
"
        
self
.
_level
=
None
        
self
.
_fingerprint
=
None
        
self
.
_transaction
=
None
        
self
.
_transaction_info
=
{
}
        
self
.
_user
=
None
        
self
.
_tags
=
{
}
        
self
.
_contexts
=
{
}
        
self
.
_extras
=
{
}
        
self
.
_attachments
=
[
]
        
self
.
clear_breadcrumbs
(
)
        
self
.
_should_capture
=
True
        
self
.
_span
=
None
        
self
.
_session
=
None
        
self
.
_force_auto_session_tracking
=
None
        
self
.
_profile
=
None
        
self
.
_propagation_context
=
None
        
self
.
_last_event_id
=
None
        
self
.
_flags
=
None
    
_attr_setter
    
def
level
(
self
value
)
:
        
"
"
"
        
When
set
this
overrides
the
level
.
        
.
.
deprecated
:
:
1
.
0
.
0
            
Use
:
func
:
set_level
instead
.
        
:
param
value
:
The
level
to
set
.
        
"
"
"
        
logger
.
warning
(
            
"
Deprecated
:
use
.
set_level
(
)
instead
.
This
will
be
removed
in
the
future
.
"
        
)
        
self
.
_level
=
value
    
def
set_level
(
self
value
)
:
        
"
"
"
        
Sets
the
level
for
the
scope
.
        
:
param
value
:
The
level
to
set
.
        
"
"
"
        
self
.
_level
=
value
    
_attr_setter
    
def
fingerprint
(
self
value
)
:
        
"
"
"
When
set
this
overrides
the
default
fingerprint
.
"
"
"
        
self
.
_fingerprint
=
value
    
property
    
def
transaction
(
self
)
:
        
"
"
"
Return
the
transaction
(
root
span
)
in
the
scope
if
any
.
"
"
"
        
if
self
.
_span
is
None
:
            
return
None
        
if
self
.
_span
.
containing_transaction
is
None
:
            
return
None
        
return
self
.
_span
.
containing_transaction
    
transaction
.
setter
    
def
transaction
(
self
value
)
:
        
"
"
"
When
set
this
forces
a
specific
transaction
name
to
be
set
.
        
Deprecated
:
use
set_transaction_name
instead
.
"
"
"
        
logger
.
warning
(
            
"
Assigning
to
scope
.
transaction
directly
is
deprecated
:
use
scope
.
set_transaction_name
(
)
instead
.
"
        
)
        
self
.
_transaction
=
value
        
if
self
.
_span
and
self
.
_span
.
containing_transaction
:
            
self
.
_span
.
containing_transaction
.
name
=
value
    
def
set_transaction_name
(
self
name
source
=
None
)
:
        
"
"
"
Set
the
transaction
name
and
optionally
the
transaction
source
.
"
"
"
        
self
.
_transaction
=
name
        
if
self
.
_span
and
self
.
_span
.
containing_transaction
:
            
self
.
_span
.
containing_transaction
.
name
=
name
            
if
source
:
                
self
.
_span
.
containing_transaction
.
source
=
source
        
if
source
:
            
self
.
_transaction_info
[
"
source
"
]
=
source
    
_attr_setter
    
def
user
(
self
value
)
:
        
"
"
"
When
set
a
specific
user
is
bound
to
the
scope
.
Deprecated
in
favor
of
set_user
.
"
"
"
        
warnings
.
warn
(
            
"
The
Scope
.
user
setter
is
deprecated
in
favor
of
Scope
.
set_user
(
)
.
"
            
DeprecationWarning
            
stacklevel
=
2
        
)
        
self
.
set_user
(
value
)
    
def
set_user
(
self
value
)
:
        
"
"
"
Sets
a
user
for
the
scope
.
"
"
"
        
self
.
_user
=
value
        
session
=
self
.
get_isolation_scope
(
)
.
_session
        
if
session
is
not
None
:
            
session
.
update
(
user
=
value
)
    
property
    
def
span
(
self
)
:
        
"
"
"
Get
/
set
current
tracing
span
or
transaction
.
"
"
"
        
return
self
.
_span
    
span
.
setter
    
def
span
(
self
span
)
:
        
self
.
_span
=
span
        
if
isinstance
(
span
Transaction
)
:
            
transaction
=
span
            
if
transaction
.
name
:
                
self
.
_transaction
=
transaction
.
name
                
if
transaction
.
source
:
                    
self
.
_transaction_info
[
"
source
"
]
=
transaction
.
source
    
property
    
def
profile
(
self
)
:
        
return
self
.
_profile
    
profile
.
setter
    
def
profile
(
self
profile
)
:
        
self
.
_profile
=
profile
    
def
set_tag
(
self
key
value
)
:
        
"
"
"
        
Sets
a
tag
for
a
key
to
a
specific
value
.
        
:
param
key
:
Key
of
the
tag
to
set
.
        
:
param
value
:
Value
of
the
tag
to
set
.
        
"
"
"
        
self
.
_tags
[
key
]
=
value
    
def
set_tags
(
self
tags
)
:
        
"
"
"
Sets
multiple
tags
at
once
.
        
This
method
updates
multiple
tags
at
once
.
The
tags
are
passed
as
a
dictionary
        
or
other
mapping
type
.
        
Calling
this
method
is
equivalent
to
calling
set_tag
on
each
key
-
value
pair
        
in
the
mapping
.
If
a
tag
key
already
exists
in
the
scope
its
value
will
be
        
updated
.
If
the
tag
key
does
not
exist
in
the
scope
the
key
-
value
pair
will
        
be
added
to
the
scope
.
        
This
method
only
modifies
tag
keys
in
the
tags
mapping
passed
to
the
method
.
        
scope
.
set_tags
(
{
}
)
is
therefore
a
no
-
op
.
        
:
param
tags
:
A
mapping
of
tag
keys
to
tag
values
to
set
.
        
"
"
"
        
self
.
_tags
.
update
(
tags
)
    
def
remove_tag
(
self
key
)
:
        
"
"
"
        
Removes
a
specific
tag
.
        
:
param
key
:
Key
of
the
tag
to
remove
.
        
"
"
"
        
self
.
_tags
.
pop
(
key
None
)
    
def
set_context
(
        
self
        
key
        
value
    
)
:
        
"
"
"
        
Binds
a
context
at
a
certain
key
to
a
specific
value
.
        
"
"
"
        
self
.
_contexts
[
key
]
=
value
    
def
remove_context
(
        
self
key
    
)
:
        
"
"
"
Removes
a
context
.
"
"
"
        
self
.
_contexts
.
pop
(
key
None
)
    
def
set_extra
(
        
self
        
key
        
value
    
)
:
        
"
"
"
Sets
an
extra
key
to
a
specific
value
.
"
"
"
        
self
.
_extras
[
key
]
=
value
    
def
remove_extra
(
        
self
key
    
)
:
        
"
"
"
Removes
a
specific
extra
key
.
"
"
"
        
self
.
_extras
.
pop
(
key
None
)
    
def
clear_breadcrumbs
(
self
)
:
        
"
"
"
Clears
breadcrumb
buffer
.
"
"
"
        
self
.
_breadcrumbs
=
deque
(
)
        
self
.
_n_breadcrumbs_truncated
=
0
    
def
add_attachment
(
        
self
        
bytes
=
None
        
filename
=
None
        
path
=
None
        
content_type
=
None
        
add_to_transactions
=
False
    
)
:
        
"
"
"
Adds
an
attachment
to
future
events
sent
from
this
scope
.
        
The
parameters
are
the
same
as
for
the
:
py
:
class
:
sentry_sdk
.
attachments
.
Attachment
constructor
.
        
"
"
"
        
self
.
_attachments
.
append
(
            
Attachment
(
                
bytes
=
bytes
                
path
=
path
                
filename
=
filename
                
content_type
=
content_type
                
add_to_transactions
=
add_to_transactions
            
)
        
)
    
def
add_breadcrumb
(
self
crumb
=
None
hint
=
None
*
*
kwargs
)
:
        
"
"
"
        
Adds
a
breadcrumb
.
        
:
param
crumb
:
Dictionary
with
the
data
as
the
sentry
v7
/
v8
protocol
expects
.
        
:
param
hint
:
An
optional
value
that
can
be
used
by
before_breadcrumb
            
to
customize
the
breadcrumbs
that
are
emitted
.
        
"
"
"
        
client
=
self
.
get_client
(
)
        
if
not
client
.
is_active
(
)
:
            
logger
.
info
(
"
Dropped
breadcrumb
because
no
client
bound
"
)
            
return
        
before_breadcrumb
=
client
.
options
.
get
(
"
before_breadcrumb
"
)
        
max_breadcrumbs
=
client
.
options
.
get
(
"
max_breadcrumbs
"
DEFAULT_MAX_BREADCRUMBS
)
        
crumb
=
dict
(
crumb
or
(
)
)
        
crumb
.
update
(
kwargs
)
        
if
not
crumb
:
            
return
        
hint
=
dict
(
hint
or
(
)
)
        
if
crumb
.
get
(
"
timestamp
"
)
is
None
:
            
crumb
[
"
timestamp
"
]
=
datetime
.
now
(
timezone
.
utc
)
        
if
crumb
.
get
(
"
type
"
)
is
None
:
            
crumb
[
"
type
"
]
=
"
default
"
        
if
before_breadcrumb
is
not
None
:
            
new_crumb
=
before_breadcrumb
(
crumb
hint
)
        
else
:
            
new_crumb
=
crumb
        
if
new_crumb
is
not
None
:
            
self
.
_breadcrumbs
.
append
(
new_crumb
)
        
else
:
            
logger
.
info
(
"
before
breadcrumb
dropped
breadcrumb
(
%
s
)
"
crumb
)
        
while
len
(
self
.
_breadcrumbs
)
>
max_breadcrumbs
:
            
self
.
_breadcrumbs
.
popleft
(
)
            
self
.
_n_breadcrumbs_truncated
+
=
1
    
def
start_transaction
(
        
self
        
transaction
=
None
        
instrumenter
=
INSTRUMENTER
.
SENTRY
        
custom_sampling_context
=
None
        
*
*
kwargs
    
)
:
        
"
"
"
        
Start
and
return
a
transaction
.
        
Start
an
existing
transaction
if
given
otherwise
create
and
start
a
new
        
transaction
with
kwargs
.
        
This
is
the
entry
point
to
manual
tracing
instrumentation
.
        
A
tree
structure
can
be
built
by
adding
child
spans
to
the
transaction
        
and
child
spans
to
other
spans
.
To
start
a
new
child
span
within
the
        
transaction
or
any
span
call
the
respective
.
start_child
(
)
method
.
        
Every
child
span
must
be
finished
before
the
transaction
is
finished
        
otherwise
the
unfinished
spans
are
discarded
.
        
When
used
as
context
managers
spans
and
transactions
are
automatically
        
finished
at
the
end
of
the
with
block
.
If
not
using
context
managers
        
call
the
.
finish
(
)
method
.
        
When
the
transaction
is
finished
it
will
be
sent
to
Sentry
with
all
its
        
finished
child
spans
.
        
:
param
transaction
:
The
transaction
to
start
.
If
omitted
we
create
and
            
start
a
new
transaction
.
        
:
param
instrumenter
:
This
parameter
is
meant
for
internal
use
only
.
It
            
will
be
removed
in
the
next
major
version
.
        
:
param
custom_sampling_context
:
The
transaction
'
s
custom
sampling
context
.
        
:
param
kwargs
:
Optional
keyword
arguments
to
be
passed
to
the
Transaction
            
constructor
.
See
:
py
:
class
:
sentry_sdk
.
tracing
.
Transaction
for
            
available
arguments
.
        
"
"
"
        
kwargs
.
setdefault
(
"
scope
"
self
)
        
client
=
self
.
get_client
(
)
        
configuration_instrumenter
=
client
.
options
[
"
instrumenter
"
]
        
if
instrumenter
!
=
configuration_instrumenter
:
            
return
NoOpSpan
(
)
        
try_autostart_continuous_profiler
(
)
        
custom_sampling_context
=
custom_sampling_context
or
{
}
        
transaction_kwargs
=
kwargs
        
if
transaction
is
None
:
            
transaction
=
Transaction
(
*
*
transaction_kwargs
)
        
sampling_context
=
{
            
"
transaction_context
"
:
transaction
.
to_json
(
)
            
"
parent_sampled
"
:
transaction
.
parent_sampled
        
}
        
sampling_context
.
update
(
custom_sampling_context
)
        
transaction
.
_set_initial_sampling_decision
(
sampling_context
=
sampling_context
)
        
if
transaction
.
sample_rate
is
not
None
:
            
propagation_context
=
self
.
get_active_propagation_context
(
)
            
if
propagation_context
:
                
dsc
=
propagation_context
.
dynamic_sampling_context
                
if
dsc
is
not
None
:
                    
dsc
[
"
sample_rate
"
]
=
str
(
transaction
.
sample_rate
)
            
if
transaction
.
_baggage
:
                
transaction
.
_baggage
.
sentry_items
[
"
sample_rate
"
]
=
str
(
                    
transaction
.
sample_rate
                
)
        
if
transaction
.
sampled
:
            
profile
=
Profile
(
                
transaction
.
sampled
transaction
.
_start_timestamp_monotonic_ns
            
)
            
profile
.
_set_initial_sampling_decision
(
sampling_context
=
sampling_context
)
            
transaction
.
_profile
=
profile
            
transaction
.
_continuous_profile
=
try_profile_lifecycle_trace_start
(
)
            
if
transaction
.
_continuous_profile
is
not
None
:
                
transaction
.
set_profiler_id
(
get_profiler_id
(
)
)
            
max_spans
=
(
client
.
options
[
"
_experiments
"
]
.
get
(
"
max_spans
"
)
)
or
1000
            
transaction
.
init_span_recorder
(
maxlen
=
max_spans
)
        
return
transaction
    
def
start_span
(
self
instrumenter
=
INSTRUMENTER
.
SENTRY
*
*
kwargs
)
:
        
"
"
"
        
Start
a
span
whose
parent
is
the
currently
active
span
or
transaction
if
any
.
        
The
return
value
is
a
:
py
:
class
:
sentry_sdk
.
tracing
.
Span
instance
        
typically
used
as
a
context
manager
to
start
and
stop
timing
in
a
with
        
block
.
        
Only
spans
contained
in
a
transaction
are
sent
to
Sentry
.
Most
        
integrations
start
a
transaction
at
the
appropriate
time
for
example
        
for
every
incoming
HTTP
request
.
Use
        
:
py
:
meth
:
sentry_sdk
.
start_transaction
to
start
a
new
transaction
when
        
one
is
not
already
in
progress
.
        
For
supported
*
*
kwargs
see
:
py
:
class
:
sentry_sdk
.
tracing
.
Span
.
        
The
instrumenter
parameter
is
deprecated
for
user
code
and
it
will
        
be
removed
in
the
next
major
version
.
Going
forward
it
should
only
        
be
used
by
the
SDK
itself
.
        
"
"
"
        
if
kwargs
.
get
(
"
description
"
)
is
not
None
:
            
warnings
.
warn
(
                
"
The
description
parameter
is
deprecated
.
Please
use
name
instead
.
"
                
DeprecationWarning
                
stacklevel
=
2
            
)
        
with
new_scope
(
)
:
            
kwargs
.
setdefault
(
"
scope
"
self
)
            
client
=
self
.
get_client
(
)
            
configuration_instrumenter
=
client
.
options
[
"
instrumenter
"
]
            
if
instrumenter
!
=
configuration_instrumenter
:
                
return
NoOpSpan
(
)
            
span
=
self
.
span
or
self
.
get_isolation_scope
(
)
.
span
            
if
span
is
None
:
                
if
"
trace_id
"
not
in
kwargs
:
                    
propagation_context
=
self
.
get_active_propagation_context
(
)
                    
if
propagation_context
is
not
None
:
                        
kwargs
[
"
trace_id
"
]
=
propagation_context
.
trace_id
                
span
=
Span
(
*
*
kwargs
)
            
else
:
                
span
=
span
.
start_child
(
*
*
kwargs
)
            
return
span
    
def
continue_trace
(
        
self
environ_or_headers
op
=
None
name
=
None
source
=
None
origin
=
"
manual
"
    
)
:
        
"
"
"
        
Sets
the
propagation
context
from
environment
or
headers
and
returns
a
transaction
.
        
"
"
"
        
self
.
generate_propagation_context
(
environ_or_headers
)
        
sample_rand
=
typing
.
cast
(
            
PropagationContext
self
.
_propagation_context
        
)
.
_sample_rand
(
)
        
transaction
=
Transaction
.
continue_from_headers
(
            
normalize_incoming_data
(
environ_or_headers
)
            
_sample_rand
=
sample_rand
            
op
=
op
            
origin
=
origin
            
name
=
name
            
source
=
source
        
)
        
return
transaction
    
def
capture_event
(
self
event
hint
=
None
scope
=
None
*
*
scope_kwargs
)
:
        
"
"
"
        
Captures
an
event
.
        
Merges
given
scope
data
and
calls
:
py
:
meth
:
sentry_sdk
.
client
.
_Client
.
capture_event
.
        
:
param
event
:
A
ready
-
made
event
that
can
be
directly
sent
to
Sentry
.
        
:
param
hint
:
Contains
metadata
about
the
event
that
can
be
read
from
before_send
such
as
the
original
exception
object
or
a
HTTP
request
object
.
        
:
param
scope
:
An
optional
:
py
:
class
:
sentry_sdk
.
Scope
to
apply
to
events
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
param
scope_kwargs
:
Optional
data
to
apply
to
event
.
            
For
supported
*
*
scope_kwargs
see
:
py
:
meth
:
sentry_sdk
.
Scope
.
update_from_kwargs
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
returns
:
An
event_id
if
the
SDK
decided
to
send
the
event
(
see
:
py
:
meth
:
sentry_sdk
.
client
.
_Client
.
capture_event
)
.
        
"
"
"
        
if
disable_capture_event
.
get
(
False
)
:
            
return
None
        
scope
=
self
.
_merge_scopes
(
scope
scope_kwargs
)
        
event_id
=
self
.
get_client
(
)
.
capture_event
(
event
=
event
hint
=
hint
scope
=
scope
)
        
if
event_id
is
not
None
and
event
.
get
(
"
type
"
)
!
=
"
transaction
"
:
            
self
.
get_isolation_scope
(
)
.
_last_event_id
=
event_id
        
return
event_id
    
def
capture_message
(
self
message
level
=
None
scope
=
None
*
*
scope_kwargs
)
:
        
"
"
"
        
Captures
a
message
.
        
:
param
message
:
The
string
to
send
as
the
message
.
        
:
param
level
:
If
no
level
is
provided
the
default
level
is
info
.
        
:
param
scope
:
An
optional
:
py
:
class
:
sentry_sdk
.
Scope
to
apply
to
events
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
param
scope_kwargs
:
Optional
data
to
apply
to
event
.
            
For
supported
*
*
scope_kwargs
see
:
py
:
meth
:
sentry_sdk
.
Scope
.
update_from_kwargs
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
returns
:
An
event_id
if
the
SDK
decided
to
send
the
event
(
see
:
py
:
meth
:
sentry_sdk
.
client
.
_Client
.
capture_event
)
.
        
"
"
"
        
if
disable_capture_event
.
get
(
False
)
:
            
return
None
        
if
level
is
None
:
            
level
=
"
info
"
        
event
=
{
            
"
message
"
:
message
            
"
level
"
:
level
        
}
        
return
self
.
capture_event
(
event
scope
=
scope
*
*
scope_kwargs
)
    
def
capture_exception
(
self
error
=
None
scope
=
None
*
*
scope_kwargs
)
:
        
"
"
"
Captures
an
exception
.
        
:
param
error
:
An
exception
to
capture
.
If
None
sys
.
exc_info
(
)
will
be
used
.
        
:
param
scope
:
An
optional
:
py
:
class
:
sentry_sdk
.
Scope
to
apply
to
events
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
param
scope_kwargs
:
Optional
data
to
apply
to
event
.
            
For
supported
*
*
scope_kwargs
see
:
py
:
meth
:
sentry_sdk
.
Scope
.
update_from_kwargs
.
            
The
scope
and
scope_kwargs
parameters
are
mutually
exclusive
.
        
:
returns
:
An
event_id
if
the
SDK
decided
to
send
the
event
(
see
:
py
:
meth
:
sentry_sdk
.
client
.
_Client
.
capture_event
)
.
        
"
"
"
        
if
disable_capture_event
.
get
(
False
)
:
            
return
None
        
if
error
is
not
None
:
            
exc_info
=
exc_info_from_error
(
error
)
        
else
:
            
exc_info
=
sys
.
exc_info
(
)
        
event
hint
=
event_from_exception
(
            
exc_info
client_options
=
self
.
get_client
(
)
.
options
        
)
        
try
:
            
return
self
.
capture_event
(
event
hint
=
hint
scope
=
scope
*
*
scope_kwargs
)
        
except
Exception
:
            
capture_internal_exception
(
sys
.
exc_info
(
)
)
        
return
None
    
def
start_session
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
Starts
a
new
session
.
"
"
"
        
session_mode
=
kwargs
.
pop
(
"
session_mode
"
"
application
"
)
        
self
.
end_session
(
)
        
client
=
self
.
get_client
(
)
        
self
.
_session
=
Session
(
            
release
=
client
.
options
.
get
(
"
release
"
)
            
environment
=
client
.
options
.
get
(
"
environment
"
)
            
user
=
self
.
_user
            
session_mode
=
session_mode
        
)
    
def
end_session
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
Ends
the
current
session
if
there
is
one
.
"
"
"
        
session
=
self
.
_session
        
self
.
_session
=
None
        
if
session
is
not
None
:
            
session
.
close
(
)
            
self
.
get_client
(
)
.
capture_session
(
session
)
    
def
stop_auto_session_tracking
(
self
*
args
*
*
kwargs
)
:
        
"
"
"
Stops
automatic
session
tracking
.
        
This
temporarily
session
tracking
for
the
current
scope
when
called
.
        
To
resume
session
tracking
call
resume_auto_session_tracking
.
        
"
"
"
        
self
.
end_session
(
)
        
self
.
_force_auto_session_tracking
=
False
    
def
resume_auto_session_tracking
(
self
)
:
        
"
"
"
Resumes
automatic
session
tracking
for
the
current
scope
if
        
disabled
earlier
.
This
requires
that
generally
automatic
session
        
tracking
is
enabled
.
        
"
"
"
        
self
.
_force_auto_session_tracking
=
None
    
def
add_event_processor
(
        
self
func
    
)
:
        
"
"
"
Register
a
scope
local
event
processor
on
the
scope
.
        
:
param
func
:
This
function
behaves
like
before_send
.
        
"
"
"
        
if
len
(
self
.
_event_processors
)
>
20
:
            
logger
.
warning
(
                
"
Too
many
event
processors
on
scope
!
Clearing
list
to
free
up
some
memory
:
%
r
"
                
self
.
_event_processors
            
)
            
del
self
.
_event_processors
[
:
]
        
self
.
_event_processors
.
append
(
func
)
    
def
add_error_processor
(
        
self
        
func
        
cls
=
None
    
)
:
        
"
"
"
Register
a
scope
local
error
processor
on
the
scope
.
        
:
param
func
:
A
callback
that
works
similar
to
an
event
processor
but
is
invoked
with
the
original
exception
info
triple
as
second
argument
.
        
:
param
cls
:
Optionally
only
process
exceptions
of
this
type
.
        
"
"
"
        
if
cls
is
not
None
:
            
cls_
=
cls
            
real_func
=
func
            
def
func
(
event
exc_info
)
:
                
try
:
                    
is_inst
=
isinstance
(
exc_info
[
1
]
cls_
)
                
except
Exception
:
                    
is_inst
=
False
                
if
is_inst
:
                    
return
real_func
(
event
exc_info
)
                
return
event
        
self
.
_error_processors
.
append
(
func
)
    
def
_apply_level_to_event
(
self
event
hint
options
)
:
        
if
self
.
_level
is
not
None
:
            
event
[
"
level
"
]
=
self
.
_level
    
def
_apply_breadcrumbs_to_event
(
self
event
hint
options
)
:
        
event
.
setdefault
(
"
breadcrumbs
"
{
}
)
        
if
not
isinstance
(
event
[
"
breadcrumbs
"
]
AnnotatedValue
)
:
            
event
[
"
breadcrumbs
"
]
.
setdefault
(
"
values
"
[
]
)
            
event
[
"
breadcrumbs
"
]
[
"
values
"
]
.
extend
(
self
.
_breadcrumbs
)
        
try
:
            
if
not
isinstance
(
event
[
"
breadcrumbs
"
]
AnnotatedValue
)
:
                
for
crumb
in
event
[
"
breadcrumbs
"
]
[
"
values
"
]
:
                    
if
isinstance
(
crumb
[
"
timestamp
"
]
str
)
:
                        
crumb
[
"
timestamp
"
]
=
datetime_from_isoformat
(
crumb
[
"
timestamp
"
]
)
                
event
[
"
breadcrumbs
"
]
[
"
values
"
]
.
sort
(
                    
key
=
lambda
crumb
:
crumb
[
"
timestamp
"
]
                
)
        
except
Exception
as
err
:
            
logger
.
debug
(
"
Error
when
sorting
breadcrumbs
"
exc_info
=
err
)
            
pass
    
def
_apply_user_to_event
(
self
event
hint
options
)
:
        
if
event
.
get
(
"
user
"
)
is
None
and
self
.
_user
is
not
None
:
            
event
[
"
user
"
]
=
self
.
_user
    
def
_apply_transaction_name_to_event
(
self
event
hint
options
)
:
        
if
event
.
get
(
"
transaction
"
)
is
None
and
self
.
_transaction
is
not
None
:
            
event
[
"
transaction
"
]
=
self
.
_transaction
    
def
_apply_transaction_info_to_event
(
self
event
hint
options
)
:
        
if
event
.
get
(
"
transaction_info
"
)
is
None
and
self
.
_transaction_info
is
not
None
:
            
event
[
"
transaction_info
"
]
=
self
.
_transaction_info
    
def
_apply_fingerprint_to_event
(
self
event
hint
options
)
:
        
if
event
.
get
(
"
fingerprint
"
)
is
None
and
self
.
_fingerprint
is
not
None
:
            
event
[
"
fingerprint
"
]
=
self
.
_fingerprint
    
def
_apply_extra_to_event
(
self
event
hint
options
)
:
        
if
self
.
_extras
:
            
event
.
setdefault
(
"
extra
"
{
}
)
.
update
(
self
.
_extras
)
    
def
_apply_tags_to_event
(
self
event
hint
options
)
:
        
if
self
.
_tags
:
            
event
.
setdefault
(
"
tags
"
{
}
)
.
update
(
self
.
_tags
)
    
def
_apply_contexts_to_event
(
self
event
hint
options
)
:
        
if
self
.
_contexts
:
            
event
.
setdefault
(
"
contexts
"
{
}
)
.
update
(
self
.
_contexts
)
        
contexts
=
event
.
setdefault
(
"
contexts
"
{
}
)
        
if
contexts
.
get
(
"
trace
"
)
is
None
:
            
if
has_tracing_enabled
(
options
)
and
self
.
_span
is
not
None
:
                
contexts
[
"
trace
"
]
=
self
.
_span
.
get_trace_context
(
)
            
else
:
                
contexts
[
"
trace
"
]
=
self
.
get_trace_context
(
)
    
def
_apply_flags_to_event
(
self
event
hint
options
)
:
        
flags
=
self
.
flags
.
get
(
)
        
if
len
(
flags
)
>
0
:
            
event
.
setdefault
(
"
contexts
"
{
}
)
.
setdefault
(
"
flags
"
{
}
)
.
update
(
                
{
"
values
"
:
flags
}
            
)
    
def
_drop
(
self
cause
ty
)
:
        
logger
.
info
(
"
%
s
(
%
s
)
dropped
event
"
ty
cause
)
        
return
None
    
def
run_error_processors
(
self
event
hint
)
:
        
"
"
"
        
Runs
the
error
processors
on
the
event
and
returns
the
modified
event
.
        
"
"
"
        
exc_info
=
hint
.
get
(
"
exc_info
"
)
        
if
exc_info
is
not
None
:
            
error_processors
=
chain
(
                
self
.
get_global_scope
(
)
.
_error_processors
                
self
.
get_isolation_scope
(
)
.
_error_processors
                
self
.
get_current_scope
(
)
.
_error_processors
            
)
            
for
error_processor
in
error_processors
:
                
new_event
=
error_processor
(
event
exc_info
)
                
if
new_event
is
None
:
                    
return
self
.
_drop
(
error_processor
"
error
processor
"
)
                
event
=
new_event
        
return
event
    
def
run_event_processors
(
self
event
hint
)
:
        
"
"
"
        
Runs
the
event
processors
on
the
event
and
returns
the
modified
event
.
        
"
"
"
        
ty
=
event
.
get
(
"
type
"
)
        
is_check_in
=
ty
=
=
"
check_in
"
        
if
not
is_check_in
:
            
isolation_scope
=
_isolation_scope
.
get
(
)
            
current_scope
=
_current_scope
.
get
(
)
            
event_processors
=
chain
(
                
global_event_processors
                
_global_scope
and
_global_scope
.
_event_processors
or
[
]
                
isolation_scope
and
isolation_scope
.
_event_processors
or
[
]
                
current_scope
and
current_scope
.
_event_processors
or
[
]
            
)
            
for
event_processor
in
event_processors
:
                
new_event
=
event
                
with
capture_internal_exceptions
(
)
:
                    
new_event
=
event_processor
(
event
hint
)
                
if
new_event
is
None
:
                    
return
self
.
_drop
(
event_processor
"
event
processor
"
)
                
event
=
new_event
        
return
event
    
_disable_capture
    
def
apply_to_event
(
        
self
        
event
        
hint
        
options
=
None
    
)
:
        
"
"
"
Applies
the
information
contained
on
the
scope
to
the
given
event
.
"
"
"
        
ty
=
event
.
get
(
"
type
"
)
        
is_transaction
=
ty
=
=
"
transaction
"
        
is_check_in
=
ty
=
=
"
check_in
"
        
attachments_to_send
=
hint
.
get
(
"
attachments
"
)
or
[
]
        
for
attachment
in
self
.
_attachments
:
            
if
not
is_transaction
or
attachment
.
add_to_transactions
:
                
attachments_to_send
.
append
(
attachment
)
        
hint
[
"
attachments
"
]
=
attachments_to_send
        
self
.
_apply_contexts_to_event
(
event
hint
options
)
        
if
is_check_in
:
            
event
[
"
contexts
"
]
=
{
                
"
trace
"
:
event
.
setdefault
(
"
contexts
"
{
}
)
.
get
(
"
trace
"
{
}
)
            
}
        
if
not
is_check_in
:
            
self
.
_apply_level_to_event
(
event
hint
options
)
            
self
.
_apply_fingerprint_to_event
(
event
hint
options
)
            
self
.
_apply_user_to_event
(
event
hint
options
)
            
self
.
_apply_transaction_name_to_event
(
event
hint
options
)
            
self
.
_apply_transaction_info_to_event
(
event
hint
options
)
            
self
.
_apply_tags_to_event
(
event
hint
options
)
            
self
.
_apply_extra_to_event
(
event
hint
options
)
        
if
not
is_transaction
and
not
is_check_in
:
            
self
.
_apply_breadcrumbs_to_event
(
event
hint
options
)
            
self
.
_apply_flags_to_event
(
event
hint
options
)
        
event
=
self
.
run_error_processors
(
event
hint
)
        
if
event
is
None
:
            
return
None
        
event
=
self
.
run_event_processors
(
event
hint
)
        
if
event
is
None
:
            
return
None
        
return
event
    
def
update_from_scope
(
self
scope
)
:
        
"
"
"
Update
the
scope
with
another
scope
'
s
data
.
"
"
"
        
if
scope
.
_level
is
not
None
:
            
self
.
_level
=
scope
.
_level
        
if
scope
.
_fingerprint
is
not
None
:
            
self
.
_fingerprint
=
scope
.
_fingerprint
        
if
scope
.
_transaction
is
not
None
:
            
self
.
_transaction
=
scope
.
_transaction
        
if
scope
.
_transaction_info
is
not
None
:
            
self
.
_transaction_info
.
update
(
scope
.
_transaction_info
)
        
if
scope
.
_user
is
not
None
:
            
self
.
_user
=
scope
.
_user
        
if
scope
.
_tags
:
            
self
.
_tags
.
update
(
scope
.
_tags
)
        
if
scope
.
_contexts
:
            
self
.
_contexts
.
update
(
scope
.
_contexts
)
        
if
scope
.
_extras
:
            
self
.
_extras
.
update
(
scope
.
_extras
)
        
if
scope
.
_breadcrumbs
:
            
self
.
_breadcrumbs
.
extend
(
scope
.
_breadcrumbs
)
        
if
scope
.
_n_breadcrumbs_truncated
:
            
self
.
_n_breadcrumbs_truncated
=
(
                
self
.
_n_breadcrumbs_truncated
+
scope
.
_n_breadcrumbs_truncated
            
)
        
if
scope
.
_span
:
            
self
.
_span
=
scope
.
_span
        
if
scope
.
_attachments
:
            
self
.
_attachments
.
extend
(
scope
.
_attachments
)
        
if
scope
.
_profile
:
            
self
.
_profile
=
scope
.
_profile
        
if
scope
.
_propagation_context
:
            
self
.
_propagation_context
=
scope
.
_propagation_context
        
if
scope
.
_session
:
            
self
.
_session
=
scope
.
_session
        
if
scope
.
_flags
:
            
if
not
self
.
_flags
:
                
self
.
_flags
=
deepcopy
(
scope
.
_flags
)
            
else
:
                
for
flag
in
scope
.
_flags
.
get
(
)
:
                    
self
.
_flags
.
set
(
flag
[
"
flag
"
]
flag
[
"
result
"
]
)
    
def
update_from_kwargs
(
        
self
        
user
=
None
        
level
=
None
        
extras
=
None
        
contexts
=
None
        
tags
=
None
        
fingerprint
=
None
    
)
:
        
"
"
"
Update
the
scope
'
s
attributes
.
"
"
"
        
if
level
is
not
None
:
            
self
.
_level
=
level
        
if
user
is
not
None
:
            
self
.
_user
=
user
        
if
extras
is
not
None
:
            
self
.
_extras
.
update
(
extras
)
        
if
contexts
is
not
None
:
            
self
.
_contexts
.
update
(
contexts
)
        
if
tags
is
not
None
:
            
self
.
_tags
.
update
(
tags
)
        
if
fingerprint
is
not
None
:
            
self
.
_fingerprint
=
fingerprint
    
def
__repr__
(
self
)
:
        
return
"
<
%
s
id
=
%
s
name
=
%
s
type
=
%
s
>
"
%
(
            
self
.
__class__
.
__name__
            
hex
(
id
(
self
)
)
            
self
.
_name
            
self
.
_type
        
)
    
property
    
def
flags
(
self
)
:
        
if
self
.
_flags
is
None
:
            
max_flags
=
(
                
self
.
get_client
(
)
.
options
[
"
_experiments
"
]
.
get
(
"
max_flags
"
)
                
or
DEFAULT_FLAG_CAPACITY
            
)
            
self
.
_flags
=
FlagBuffer
(
capacity
=
max_flags
)
        
return
self
.
_flags
contextmanager
def
new_scope
(
)
:
    
"
"
"
    
.
.
versionadded
:
:
2
.
0
.
0
    
Context
manager
that
forks
the
current
scope
and
runs
the
wrapped
code
in
it
.
    
After
the
wrapped
code
is
executed
the
original
scope
is
restored
.
    
Example
Usage
:
    
.
.
code
-
block
:
:
python
        
import
sentry_sdk
        
with
sentry_sdk
.
new_scope
(
)
as
scope
:
            
scope
.
set_tag
(
"
color
"
"
green
"
)
            
sentry_sdk
.
capture_message
(
"
hello
"
)
#
will
include
color
tag
.
        
sentry_sdk
.
capture_message
(
"
hello
again
"
)
#
will
NOT
include
color
tag
.
    
"
"
"
    
current_scope
=
Scope
.
get_current_scope
(
)
    
new_scope
=
current_scope
.
fork
(
)
    
token
=
_current_scope
.
set
(
new_scope
)
    
try
:
        
yield
new_scope
    
finally
:
        
_current_scope
.
reset
(
token
)
contextmanager
def
use_scope
(
scope
)
:
    
"
"
"
    
.
.
versionadded
:
:
2
.
0
.
0
    
Context
manager
that
uses
the
given
scope
and
runs
the
wrapped
code
in
it
.
    
After
the
wrapped
code
is
executed
the
original
scope
is
restored
.
    
Example
Usage
:
    
Suppose
the
variable
scope
contains
a
Scope
object
which
is
not
currently
    
the
active
scope
.
    
.
.
code
-
block
:
:
python
        
import
sentry_sdk
        
with
sentry_sdk
.
use_scope
(
scope
)
:
            
scope
.
set_tag
(
"
color
"
"
green
"
)
            
sentry_sdk
.
capture_message
(
"
hello
"
)
#
will
include
color
tag
.
        
sentry_sdk
.
capture_message
(
"
hello
again
"
)
#
will
NOT
include
color
tag
.
    
"
"
"
    
token
=
_current_scope
.
set
(
scope
)
    
try
:
        
yield
scope
    
finally
:
        
_current_scope
.
reset
(
token
)
contextmanager
def
isolation_scope
(
)
:
    
"
"
"
    
.
.
versionadded
:
:
2
.
0
.
0
    
Context
manager
that
forks
the
current
isolation
scope
and
runs
the
wrapped
code
in
it
.
    
The
current
scope
is
also
forked
to
not
bleed
data
into
the
existing
current
scope
.
    
After
the
wrapped
code
is
executed
the
original
scopes
are
restored
.
    
Example
Usage
:
    
.
.
code
-
block
:
:
python
        
import
sentry_sdk
        
with
sentry_sdk
.
isolation_scope
(
)
as
scope
:
            
scope
.
set_tag
(
"
color
"
"
green
"
)
            
sentry_sdk
.
capture_message
(
"
hello
"
)
#
will
include
color
tag
.
        
sentry_sdk
.
capture_message
(
"
hello
again
"
)
#
will
NOT
include
color
tag
.
    
"
"
"
    
current_scope
=
Scope
.
get_current_scope
(
)
    
forked_current_scope
=
current_scope
.
fork
(
)
    
current_token
=
_current_scope
.
set
(
forked_current_scope
)
    
isolation_scope
=
Scope
.
get_isolation_scope
(
)
    
new_isolation_scope
=
isolation_scope
.
fork
(
)
    
isolation_token
=
_isolation_scope
.
set
(
new_isolation_scope
)
    
try
:
        
yield
new_isolation_scope
    
finally
:
        
_current_scope
.
reset
(
current_token
)
        
_isolation_scope
.
reset
(
isolation_token
)
contextmanager
def
use_isolation_scope
(
isolation_scope
)
:
    
"
"
"
    
.
.
versionadded
:
:
2
.
0
.
0
    
Context
manager
that
uses
the
given
isolation_scope
and
runs
the
wrapped
code
in
it
.
    
The
current
scope
is
also
forked
to
not
bleed
data
into
the
existing
current
scope
.
    
After
the
wrapped
code
is
executed
the
original
scopes
are
restored
.
    
Example
Usage
:
    
.
.
code
-
block
:
:
python
        
import
sentry_sdk
        
with
sentry_sdk
.
isolation_scope
(
)
as
scope
:
            
scope
.
set_tag
(
"
color
"
"
green
"
)
            
sentry_sdk
.
capture_message
(
"
hello
"
)
#
will
include
color
tag
.
        
sentry_sdk
.
capture_message
(
"
hello
again
"
)
#
will
NOT
include
color
tag
.
    
"
"
"
    
current_scope
=
Scope
.
get_current_scope
(
)
    
forked_current_scope
=
current_scope
.
fork
(
)
    
current_token
=
_current_scope
.
set
(
forked_current_scope
)
    
isolation_token
=
_isolation_scope
.
set
(
isolation_scope
)
    
try
:
        
yield
isolation_scope
    
finally
:
        
_current_scope
.
reset
(
current_token
)
        
_isolation_scope
.
reset
(
isolation_token
)
def
should_send_default_pii
(
)
:
    
"
"
"
Shortcut
for
Scope
.
get_client
(
)
.
should_send_default_pii
(
)
.
"
"
"
    
return
Scope
.
get_client
(
)
.
should_send_default_pii
(
)
from
sentry_sdk
.
client
import
NonRecordingClient
if
TYPE_CHECKING
:
    
import
sentry_sdk
.
client
