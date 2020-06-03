import
re
import
uuid
import
contextlib
import
time
from
datetime
import
datetime
timedelta
import
sentry_sdk
from
sentry_sdk
.
utils
import
capture_internal_exceptions
logger
to_string
from
sentry_sdk
.
_compat
import
PY2
from
sentry_sdk
.
_types
import
MYPY
if
PY2
:
    
from
collections
import
Mapping
else
:
    
from
collections
.
abc
import
Mapping
if
MYPY
:
    
import
typing
    
from
typing
import
Generator
    
from
typing
import
Optional
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
List
    
from
typing
import
Tuple
_traceparent_header_format_re
=
re
.
compile
(
    
"
^
[
\
t
]
*
"
    
"
(
[
0
-
9a
-
f
]
{
32
}
)
?
"
    
"
-
?
(
[
0
-
9a
-
f
]
{
16
}
)
?
"
    
"
-
?
(
[
01
]
)
?
"
    
"
[
\
t
]
*
"
)
class
EnvironHeaders
(
Mapping
)
:
    
def
__init__
(
        
self
        
environ
        
prefix
=
"
HTTP_
"
    
)
:
        
self
.
environ
=
environ
        
self
.
prefix
=
prefix
    
def
__getitem__
(
self
key
)
:
        
return
self
.
environ
[
self
.
prefix
+
key
.
replace
(
"
-
"
"
_
"
)
.
upper
(
)
]
    
def
__len__
(
self
)
:
        
return
sum
(
1
for
_
in
iter
(
self
)
)
    
def
__iter__
(
self
)
:
        
for
k
in
self
.
environ
:
            
if
not
isinstance
(
k
str
)
:
                
continue
            
k
=
k
.
replace
(
"
-
"
"
_
"
)
.
upper
(
)
            
if
not
k
.
startswith
(
self
.
prefix
)
:
                
continue
            
yield
k
[
len
(
self
.
prefix
)
:
]
class
_SpanRecorder
(
object
)
:
    
__slots__
=
(
"
maxlen
"
"
finished_spans
"
"
open_span_count
"
)
    
def
__init__
(
self
maxlen
)
:
        
self
.
maxlen
=
maxlen
        
self
.
open_span_count
=
0
        
self
.
finished_spans
=
[
]
    
def
start_span
(
self
span
)
:
        
self
.
open_span_count
+
=
1
        
if
self
.
open_span_count
>
self
.
maxlen
:
            
span
.
_span_recorder
=
None
    
def
finish_span
(
self
span
)
:
        
self
.
finished_spans
.
append
(
span
)
class
Span
(
object
)
:
    
__slots__
=
(
        
"
trace_id
"
        
"
span_id
"
        
"
parent_span_id
"
        
"
same_process_as_parent
"
        
"
sampled
"
        
"
transaction
"
        
"
op
"
        
"
description
"
        
"
start_timestamp
"
        
"
_start_timestamp_monotonic
"
        
"
status
"
        
"
timestamp
"
        
"
_tags
"
        
"
_data
"
        
"
_span_recorder
"
        
"
hub
"
        
"
_context_manager_state
"
    
)
    
def
__init__
(
        
self
        
trace_id
=
None
        
span_id
=
None
        
parent_span_id
=
None
        
same_process_as_parent
=
True
        
sampled
=
None
        
transaction
=
None
        
op
=
None
        
description
=
None
        
hub
=
None
        
status
=
None
    
)
:
        
self
.
trace_id
=
trace_id
or
uuid
.
uuid4
(
)
.
hex
        
self
.
span_id
=
span_id
or
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
        
self
.
parent_span_id
=
parent_span_id
        
self
.
same_process_as_parent
=
same_process_as_parent
        
self
.
sampled
=
sampled
        
self
.
transaction
=
transaction
        
self
.
op
=
op
        
self
.
description
=
description
        
self
.
status
=
status
        
self
.
hub
=
hub
        
self
.
_tags
=
{
}
        
self
.
_data
=
{
}
        
self
.
start_timestamp
=
datetime
.
utcnow
(
)
        
try
:
            
self
.
_start_timestamp_monotonic
=
time
.
perf_counter
(
)
        
except
AttributeError
:
            
pass
        
self
.
timestamp
=
None
        
self
.
_span_recorder
=
None
    
def
init_finished_spans
(
self
maxlen
)
:
        
if
self
.
_span_recorder
is
None
:
            
self
.
_span_recorder
=
_SpanRecorder
(
maxlen
)
        
self
.
_span_recorder
.
start_span
(
self
)
    
def
__repr__
(
self
)
:
        
return
(
            
"
<
%
s
(
transaction
=
%
r
trace_id
=
%
r
span_id
=
%
r
parent_span_id
=
%
r
sampled
=
%
r
)
>
"
            
%
(
                
self
.
__class__
.
__name__
                
self
.
transaction
                
self
.
trace_id
                
self
.
span_id
                
self
.
parent_span_id
                
self
.
sampled
            
)
        
)
    
def
__enter__
(
self
)
:
        
hub
=
self
.
hub
or
sentry_sdk
.
Hub
.
current
        
_
scope
=
hub
.
_stack
[
-
1
]
        
old_span
=
scope
.
span
        
scope
.
span
=
self
        
self
.
_context_manager_state
=
(
hub
scope
old_span
)
        
return
self
    
def
__exit__
(
self
ty
value
tb
)
:
        
if
value
is
not
None
:
            
self
.
set_status
(
"
internal_error
"
)
        
hub
scope
old_span
=
self
.
_context_manager_state
        
del
self
.
_context_manager_state
        
self
.
finish
(
hub
)
        
scope
.
span
=
old_span
    
def
new_span
(
self
*
*
kwargs
)
:
        
rv
=
type
(
self
)
(
            
trace_id
=
self
.
trace_id
            
span_id
=
None
            
parent_span_id
=
self
.
span_id
            
sampled
=
self
.
sampled
            
*
*
kwargs
        
)
        
rv
.
_span_recorder
=
self
.
_span_recorder
        
return
rv
    
classmethod
    
def
continue_from_environ
(
cls
environ
)
:
        
return
cls
.
continue_from_headers
(
EnvironHeaders
(
environ
)
)
    
classmethod
    
def
continue_from_headers
(
cls
headers
)
:
        
parent
=
cls
.
from_traceparent
(
headers
.
get
(
"
sentry
-
trace
"
)
)
        
if
parent
is
None
:
            
return
cls
(
)
        
parent
.
same_process_as_parent
=
False
        
return
parent
    
def
iter_headers
(
self
)
:
        
yield
"
sentry
-
trace
"
self
.
to_traceparent
(
)
    
classmethod
    
def
from_traceparent
(
cls
traceparent
)
:
        
if
not
traceparent
:
            
return
None
        
if
traceparent
.
startswith
(
"
00
-
"
)
and
traceparent
.
endswith
(
"
-
00
"
)
:
            
traceparent
=
traceparent
[
3
:
-
3
]
        
match
=
_traceparent_header_format_re
.
match
(
str
(
traceparent
)
)
        
if
match
is
None
:
            
return
None
        
trace_id
span_id
sampled_str
=
match
.
groups
(
)
        
if
trace_id
is
not
None
:
            
trace_id
=
"
{
:
032x
}
"
.
format
(
int
(
trace_id
16
)
)
        
if
span_id
is
not
None
:
            
span_id
=
"
{
:
016x
}
"
.
format
(
int
(
span_id
16
)
)
        
if
sampled_str
:
            
sampled
=
sampled_str
!
=
"
0
"
        
else
:
            
sampled
=
None
        
return
cls
(
trace_id
=
trace_id
parent_span_id
=
span_id
sampled
=
sampled
)
    
def
to_traceparent
(
self
)
:
        
sampled
=
"
"
        
if
self
.
sampled
is
True
:
            
sampled
=
"
1
"
        
if
self
.
sampled
is
False
:
            
sampled
=
"
0
"
        
return
"
%
s
-
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
trace_id
self
.
span_id
sampled
)
    
def
to_legacy_traceparent
(
self
)
:
        
return
"
00
-
%
s
-
%
s
-
00
"
%
(
self
.
trace_id
self
.
span_id
)
    
def
set_tag
(
self
key
value
)
:
        
self
.
_tags
[
key
]
=
value
    
def
set_data
(
self
key
value
)
:
        
self
.
_data
[
key
]
=
value
    
def
set_status
(
self
value
)
:
        
self
.
status
=
value
    
def
set_http_status
(
self
http_status
)
:
        
self
.
set_tag
(
"
http
.
status_code
"
http_status
)
        
if
http_status
<
400
:
            
self
.
set_status
(
"
ok
"
)
        
elif
400
<
=
http_status
<
500
:
            
if
http_status
=
=
403
:
                
self
.
set_status
(
"
permission_denied
"
)
            
elif
http_status
=
=
404
:
                
self
.
set_status
(
"
not_found
"
)
            
elif
http_status
=
=
429
:
                
self
.
set_status
(
"
resource_exhausted
"
)
            
elif
http_status
=
=
413
:
                
self
.
set_status
(
"
failed_precondition
"
)
            
elif
http_status
=
=
401
:
                
self
.
set_status
(
"
unauthenticated
"
)
            
elif
http_status
=
=
409
:
                
self
.
set_status
(
"
already_exists
"
)
            
else
:
                
self
.
set_status
(
"
invalid_argument
"
)
        
elif
500
<
=
http_status
<
600
:
            
if
http_status
=
=
504
:
                
self
.
set_status
(
"
deadline_exceeded
"
)
            
elif
http_status
=
=
501
:
                
self
.
set_status
(
"
unimplemented
"
)
            
elif
http_status
=
=
503
:
                
self
.
set_status
(
"
unavailable
"
)
            
else
:
                
self
.
set_status
(
"
internal_error
"
)
        
else
:
            
self
.
set_status
(
"
unknown_error
"
)
    
def
is_success
(
self
)
:
        
return
self
.
status
=
=
"
ok
"
    
def
finish
(
self
hub
=
None
)
:
        
hub
=
hub
or
self
.
hub
or
sentry_sdk
.
Hub
.
current
        
if
self
.
timestamp
is
not
None
:
            
return
None
        
try
:
            
duration_seconds
=
time
.
perf_counter
(
)
-
self
.
_start_timestamp_monotonic
            
self
.
timestamp
=
self
.
start_timestamp
+
timedelta
(
seconds
=
duration_seconds
)
        
except
AttributeError
:
            
self
.
timestamp
=
datetime
.
utcnow
(
)
        
_maybe_create_breadcrumbs_from_span
(
hub
self
)
        
if
self
.
_span_recorder
is
None
:
            
return
None
        
self
.
_span_recorder
.
finish_span
(
self
)
        
if
self
.
transaction
is
None
:
            
return
None
        
client
=
hub
.
client
        
if
client
is
None
:
            
return
None
        
if
not
self
.
sampled
:
            
if
self
.
sampled
is
None
:
                
logger
.
warning
(
"
Discarding
transaction
Span
without
sampling
decision
"
)
            
return
None
        
return
hub
.
capture_event
(
            
{
                
"
type
"
:
"
transaction
"
                
"
transaction
"
:
self
.
transaction
                
"
contexts
"
:
{
"
trace
"
:
self
.
get_trace_context
(
)
}
                
"
tags
"
:
self
.
_tags
                
"
timestamp
"
:
self
.
timestamp
                
"
start_timestamp
"
:
self
.
start_timestamp
                
"
spans
"
:
[
                    
s
.
to_json
(
client
)
                    
for
s
in
self
.
_span_recorder
.
finished_spans
                    
if
s
is
not
self
                
]
            
}
        
)
    
def
to_json
(
self
client
)
:
        
rv
=
{
            
"
trace_id
"
:
self
.
trace_id
            
"
span_id
"
:
self
.
span_id
            
"
parent_span_id
"
:
self
.
parent_span_id
            
"
same_process_as_parent
"
:
self
.
same_process_as_parent
            
"
op
"
:
self
.
op
            
"
description
"
:
self
.
description
            
"
start_timestamp
"
:
self
.
start_timestamp
            
"
timestamp
"
:
self
.
timestamp
        
}
        
transaction
=
self
.
transaction
        
if
transaction
:
            
rv
[
"
transaction
"
]
=
transaction
        
if
self
.
status
:
            
self
.
_tags
[
"
status
"
]
=
self
.
status
        
tags
=
self
.
_tags
        
if
tags
:
            
rv
[
"
tags
"
]
=
tags
        
data
=
self
.
_data
        
if
data
:
            
rv
[
"
data
"
]
=
data
        
return
rv
    
def
get_trace_context
(
self
)
:
        
rv
=
{
            
"
trace_id
"
:
self
.
trace_id
            
"
span_id
"
:
self
.
span_id
            
"
parent_span_id
"
:
self
.
parent_span_id
            
"
op
"
:
self
.
op
            
"
description
"
:
self
.
description
        
}
        
if
self
.
status
:
            
rv
[
"
status
"
]
=
self
.
status
        
return
rv
def
_format_sql
(
cursor
sql
)
:
    
real_sql
=
None
    
try
:
        
if
hasattr
(
cursor
"
mogrify
"
)
:
            
real_sql
=
cursor
.
mogrify
(
sql
)
            
if
isinstance
(
real_sql
bytes
)
:
                
real_sql
=
real_sql
.
decode
(
cursor
.
connection
.
encoding
)
    
except
Exception
:
        
real_sql
=
None
    
return
real_sql
or
to_string
(
sql
)
contextlib
.
contextmanager
def
record_sql_queries
(
    
hub
    
cursor
    
query
    
params_list
    
paramstyle
    
executemany
)
:
    
if
hub
.
client
and
hub
.
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
record_sql_params
"
False
    
)
:
        
if
not
params_list
or
params_list
=
=
[
None
]
:
            
params_list
=
None
        
if
paramstyle
=
=
"
pyformat
"
:
            
paramstyle
=
"
format
"
    
else
:
        
params_list
=
None
        
paramstyle
=
None
    
query
=
_format_sql
(
cursor
query
)
    
data
=
{
}
    
if
params_list
is
not
None
:
        
data
[
"
db
.
params
"
]
=
params_list
    
if
paramstyle
is
not
None
:
        
data
[
"
db
.
paramstyle
"
]
=
paramstyle
    
if
executemany
:
        
data
[
"
db
.
executemany
"
]
=
True
    
with
capture_internal_exceptions
(
)
:
        
hub
.
add_breadcrumb
(
message
=
query
category
=
"
query
"
data
=
data
)
    
with
hub
.
start_span
(
op
=
"
db
"
description
=
query
)
as
span
:
        
for
k
v
in
data
.
items
(
)
:
            
span
.
set_data
(
k
v
)
        
yield
span
def
_maybe_create_breadcrumbs_from_span
(
hub
span
)
:
    
if
span
.
op
=
=
"
redis
"
:
        
hub
.
add_breadcrumb
(
            
message
=
span
.
description
type
=
"
redis
"
category
=
"
redis
"
data
=
span
.
_tags
        
)
    
elif
span
.
op
=
=
"
http
"
:
        
hub
.
add_breadcrumb
(
type
=
"
http
"
category
=
"
httplib
"
data
=
span
.
_data
)
    
elif
span
.
op
=
=
"
subprocess
"
:
        
hub
.
add_breadcrumb
(
            
type
=
"
subprocess
"
            
category
=
"
subprocess
"
            
message
=
span
.
description
            
data
=
span
.
_data
        
)
