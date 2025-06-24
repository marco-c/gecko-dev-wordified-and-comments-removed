from
copy
import
copy
from
collections
import
deque
from
itertools
import
chain
import
os
import
sys
import
uuid
from
sentry_sdk
.
attachments
import
Attachment
from
sentry_sdk
.
_compat
import
datetime_utcnow
from
sentry_sdk
.
consts
import
FALSE_VALUES
INSTRUMENTER
from
sentry_sdk
.
_functools
import
wraps
from
sentry_sdk
.
profiler
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
    
extract_sentrytrace_data
    
has_tracing_enabled
    
normalize_incoming_data
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
_types
import
TYPE_CHECKING
from
sentry_sdk
.
utils
import
(
    
event_from_exception
    
exc_info_from_error
    
logger
    
capture_internal_exceptions
)
if
TYPE_CHECKING
:
    
from
collections
.
abc
import
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
        
Type
    
)
    
import
sentry_sdk
    
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
global_event_processors
=
[
]
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
def
_merge_scopes
(
base
scope_change
scope_kwargs
)
:
    
if
scope_change
and
scope_kwargs
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
    
if
scope_change
is
not
None
:
        
final_scope
=
copy
(
base
)
        
if
callable
(
scope_change
)
:
            
scope_change
(
final_scope
)
        
else
:
            
final_scope
.
update_from_scope
(
scope_change
)
    
elif
scope_kwargs
:
        
final_scope
=
copy
(
base
)
        
final_scope
.
update_from_kwargs
(
*
*
scope_kwargs
)
    
else
:
        
final_scope
=
base
    
return
final_scope
class
Scope
(
object
)
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
    
)
    
def
__init__
(
self
)
:
        
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
_extract_propagation_context
(
self
data
)
:
        
context
=
{
}
        
normalized_data
=
normalize_incoming_data
(
data
)
        
baggage_header
=
normalized_data
.
get
(
BAGGAGE_HEADER_NAME
)
        
if
baggage_header
:
            
context
[
"
dynamic_sampling_context
"
]
=
Baggage
.
from_incoming_header
(
                
baggage_header
            
)
.
dynamic_sampling_context
(
)
        
sentry_trace_header
=
normalized_data
.
get
(
SENTRY_TRACE_HEADER_NAME
)
        
if
sentry_trace_header
:
            
sentrytrace_data
=
extract_sentrytrace_data
(
sentry_trace_header
)
            
if
sentrytrace_data
is
not
None
:
                
context
.
update
(
sentrytrace_data
)
        
only_baggage_no_sentry_trace
=
(
            
"
dynamic_sampling_context
"
in
context
and
"
trace_id
"
not
in
context
        
)
        
if
only_baggage_no_sentry_trace
:
            
context
.
update
(
self
.
_create_new_propagation_context
(
)
)
        
if
context
:
            
if
not
context
.
get
(
"
span_id
"
)
:
                
context
[
"
span_id
"
]
=
uuid
.
uuid4
(
)
.
hex
[
16
:
]
            
return
context
        
return
None
    
def
_create_new_propagation_context
(
self
)
:
        
return
{
            
"
trace_id
"
:
uuid
.
uuid4
(
)
.
hex
            
"
span_id
"
:
uuid
.
uuid4
(
)
.
hex
[
16
:
]
            
"
parent_span_id
"
:
None
            
"
dynamic_sampling_context
"
:
None
        
}
    
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
self
.
_create_new_propagation_context
(
)
        
logger
.
debug
(
            
"
[
Tracing
]
Create
new
propagation
context
:
%
s
"
            
self
.
_propagation_context
        
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
_propagation_context
is
set
.
        
If
there
is
incoming_data
overwrite
existing
_propagation_context
.
        
if
there
is
no
incoming_data
create
new
_propagation_context
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
            
context
=
self
.
_extract_propagation_context
(
incoming_data
)
            
if
context
is
not
None
:
                
self
.
_propagation_context
=
context
                
logger
.
debug
(
                    
"
[
Tracing
]
Extracted
propagation
context
from
incoming
data
:
%
s
"
                    
self
.
_propagation_context
                
)
        
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
[
"
dynamic_sampling_context
"
]
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
[
"
dynamic_sampling_context
"
]
    
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
kwargs
.
pop
(
"
client
"
None
)
        
if
(
            
client
is
not
None
            
and
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
        
)
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
None
:
            
return
None
        
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
[
"
trace_id
"
]
            
self
.
_propagation_context
[
"
span_id
"
]
        
)
        
return
traceparent
    
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
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
if
(
            
client
is
not
None
            
and
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
        
)
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
None
:
            
return
None
        
dynamic_sampling_context
=
self
.
_propagation_context
.
get
(
            
"
dynamic_sampling_context
"
        
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
[
"
trace_id
"
]
            
"
span_id
"
:
self
.
_propagation_context
[
"
span_id
"
]
            
"
parent_span_id
"
:
self
.
_propagation_context
[
"
parent_span_id
"
]
            
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
        
client
=
kwargs
.
pop
(
"
client
"
None
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
client
=
client
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
client
=
client
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
Data
taken
        
from
the
span
representing
the
request
if
available
or
the
current
        
span
on
the
scope
if
not
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
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
propagate_traces
=
client
and
client
.
options
[
"
propagate_traces
"
]
        
if
not
propagate_traces
:
            
return
        
span
=
span
or
self
.
span
        
if
client
and
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
        
if
self
.
_session
is
not
None
:
            
self
.
_session
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
kwargs
.
pop
(
"
client
"
None
)
        
if
client
is
None
:
            
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
datetime_utcnow
(
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
Transaction
.
        
"
"
"
        
hub
=
kwargs
.
pop
(
"
hub
"
None
)
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
configuration_instrumenter
=
client
and
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
        
custom_sampling_context
=
kwargs
.
pop
(
"
custom_sampling_context
"
{
}
)
        
if
transaction
is
None
:
            
kwargs
.
setdefault
(
"
hub
"
hub
)
            
transaction
=
Transaction
(
*
*
kwargs
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
        
profile
=
Profile
(
transaction
hub
=
hub
)
        
profile
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
sampled
:
            
max_spans
=
(
                
client
and
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
span
=
None
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
        
"
"
"
        
client
=
kwargs
.
get
(
"
client
"
None
)
        
configuration_instrumenter
=
client
and
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
        
if
isinstance
(
span
Transaction
)
or
"
transaction
"
in
kwargs
:
            
deprecation_msg
=
(
                
"
Deprecated
:
use
start_transaction
to
start
transactions
and
"
                
"
Transaction
.
start_child
to
start
spans
.
"
            
)
            
if
isinstance
(
span
Transaction
)
:
                
logger
.
warning
(
deprecation_msg
)
                
return
self
.
start_transaction
(
span
*
*
kwargs
)
            
if
"
transaction
"
in
kwargs
:
                
logger
.
warning
(
deprecation_msg
)
                
name
=
kwargs
.
pop
(
"
transaction
"
)
                
return
self
.
start_transaction
(
name
=
name
*
*
kwargs
)
        
if
span
is
not
None
:
            
deprecation_msg
=
"
Deprecated
:
passing
a
span
into
start_span
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
            
logger
.
warning
(
deprecation_msg
)
            
return
span
        
kwargs
.
pop
(
"
client
"
)
        
active_span
=
self
.
span
        
if
active_span
is
not
None
:
            
new_child_span
=
active_span
.
start_child
(
*
*
kwargs
)
            
return
new_child_span
        
if
"
trace_id
"
not
in
kwargs
:
            
traceparent
=
self
.
get_traceparent
(
)
            
trace_id
=
traceparent
.
split
(
"
-
"
)
[
0
]
if
traceparent
else
None
            
if
trace_id
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
trace_id
        
return
Span
(
*
*
kwargs
)
    
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
            
op
=
op
            
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
client
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
Client
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
client
:
The
client
to
use
for
sending
the
event
to
Sentry
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
Client
.
capture_event
)
.
        
"
"
"
        
if
client
is
None
:
            
return
None
        
scope
=
_merge_scopes
(
self
scope
scope_kwargs
)
        
return
client
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
    
def
capture_message
(
        
self
message
level
=
None
client
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
client
:
The
client
to
use
for
sending
the
event
to
Sentry
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
Client
.
capture_event
)
.
        
"
"
"
        
if
client
is
None
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
client
=
client
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
client
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
client
:
The
client
to
use
for
sending
the
event
to
Sentry
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
Client
.
capture_event
)
.
        
"
"
"
        
if
client
is
None
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
client
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
client
=
client
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
            
self
.
_capture_internal_exception
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
_capture_internal_exception
(
        
self
exc_info
    
)
:
        
"
"
"
        
Capture
an
exception
that
is
likely
caused
by
a
bug
in
the
SDK
        
itself
.
        
These
exceptions
do
not
end
up
in
Sentry
and
are
just
logged
instead
.
        
"
"
"
        
logger
.
error
(
"
Internal
error
in
sentry_sdk
"
exc_info
=
exc_info
)
    
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
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
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
client
=
client
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
[
"
release
"
]
if
client
else
None
            
environment
=
client
.
options
[
"
environment
"
]
if
client
else
None
            
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
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
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
            
if
client
is
not
None
:
                
client
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
        
client
=
kwargs
.
pop
(
"
client
"
None
)
        
self
.
end_session
(
client
=
client
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
.
setdefault
(
"
values
"
[
]
)
.
extend
(
            
self
.
_breadcrumbs
        
)
    
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
        
try
:
            
replay_id
=
contexts
[
"
trace
"
]
[
"
dynamic_sampling_context
"
]
[
"
replay_id
"
]
        
except
(
KeyError
TypeError
)
:
            
replay_id
=
None
        
if
replay_id
is
not
None
:
            
contexts
[
"
replay
"
]
=
{
                
"
replay_id
"
:
replay_id
            
}
    
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
        
def
_drop
(
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
            
for
error_processor
in
self
.
_error_processors
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
        
if
not
is_check_in
:
            
for
event_processor
in
chain
(
                
global_event_processors
self
.
_event_processors
            
)
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
__copy__
(
self
)
:
        
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
        
return
rv
    
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
        
)
