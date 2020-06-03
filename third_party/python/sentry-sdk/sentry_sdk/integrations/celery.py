from
__future__
import
absolute_import
import
functools
import
sys
from
sentry_sdk
.
hub
import
Hub
from
sentry_sdk
.
utils
import
capture_internal_exceptions
event_from_exception
from
sentry_sdk
.
tracing
import
Span
from
sentry_sdk
.
_compat
import
reraise
from
sentry_sdk
.
integrations
import
Integration
DidNotEnable
from
sentry_sdk
.
integrations
.
logging
import
ignore_logger
from
sentry_sdk
.
_types
import
MYPY
if
MYPY
:
    
from
typing
import
Any
    
from
typing
import
TypeVar
    
from
typing
import
Callable
    
from
typing
import
Optional
    
from
sentry_sdk
.
_types
import
EventProcessor
Event
Hint
ExcInfo
    
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
try
:
    
from
celery
import
VERSION
as
CELERY_VERSION
    
from
celery
.
exceptions
import
(
        
SoftTimeLimitExceeded
        
Retry
        
Ignore
        
Reject
    
)
except
ImportError
:
    
raise
DidNotEnable
(
"
Celery
not
installed
"
)
CELERY_CONTROL_FLOW_EXCEPTIONS
=
(
Retry
Ignore
Reject
)
class
CeleryIntegration
(
Integration
)
:
    
identifier
=
"
celery
"
    
def
__init__
(
self
propagate_traces
=
True
)
:
        
self
.
propagate_traces
=
propagate_traces
    
staticmethod
    
def
setup_once
(
)
:
        
if
CELERY_VERSION
<
(
3
)
:
            
raise
DidNotEnable
(
"
Celery
3
or
newer
required
.
"
)
        
import
celery
.
app
.
trace
as
trace
        
old_build_tracer
=
trace
.
build_tracer
        
def
sentry_build_tracer
(
name
task
*
args
*
*
kwargs
)
:
            
if
not
getattr
(
task
"
_sentry_is_patched
"
False
)
:
                
task
.
__call__
=
_wrap_task_call
(
task
task
.
__call__
)
                
task
.
run
=
_wrap_task_call
(
task
task
.
run
)
                
task
.
apply_async
=
_wrap_apply_async
(
task
task
.
apply_async
)
                
task
.
_sentry_is_patched
=
True
            
return
_wrap_tracer
(
task
old_build_tracer
(
name
task
*
args
*
*
kwargs
)
)
        
trace
.
build_tracer
=
sentry_build_tracer
        
_patch_worker_exit
(
)
        
ignore_logger
(
"
celery
.
worker
.
job
"
)
        
ignore_logger
(
"
celery
.
app
.
trace
"
)
        
ignore_logger
(
"
celery
.
redirected
"
)
def
_wrap_apply_async
(
task
f
)
:
    
functools
.
wraps
(
f
)
    
def
apply_async
(
*
args
*
*
kwargs
)
:
        
hub
=
Hub
.
current
        
integration
=
hub
.
get_integration
(
CeleryIntegration
)
        
if
integration
is
not
None
and
integration
.
propagate_traces
:
            
headers
=
None
            
for
key
value
in
hub
.
iter_trace_propagation_headers
(
)
:
                
if
headers
is
None
:
                    
headers
=
dict
(
kwargs
.
get
(
"
headers
"
)
or
{
}
)
                
headers
[
key
]
=
value
            
if
headers
is
not
None
:
                
kwargs
[
"
headers
"
]
=
headers
            
with
hub
.
start_span
(
op
=
"
celery
.
submit
"
description
=
task
.
name
)
:
                
return
f
(
*
args
*
*
kwargs
)
        
else
:
            
return
f
(
*
args
*
*
kwargs
)
    
return
apply_async
def
_wrap_tracer
(
task
f
)
:
    
functools
.
wraps
(
f
)
    
def
_inner
(
*
args
*
*
kwargs
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
CeleryIntegration
)
is
None
:
            
return
f
(
*
args
*
*
kwargs
)
        
with
hub
.
push_scope
(
)
as
scope
:
            
scope
.
_name
=
"
celery
"
            
scope
.
clear_breadcrumbs
(
)
            
scope
.
add_event_processor
(
_make_event_processor
(
task
*
args
*
*
kwargs
)
)
            
span
=
Span
.
continue_from_headers
(
args
[
3
]
.
get
(
"
headers
"
)
or
{
}
)
            
span
.
op
=
"
celery
.
task
"
            
span
.
transaction
=
"
unknown
celery
task
"
            
span
.
set_status
(
"
ok
"
)
            
with
capture_internal_exceptions
(
)
:
                
span
.
transaction
=
task
.
name
            
with
hub
.
start_span
(
span
)
:
                
return
f
(
*
args
*
*
kwargs
)
    
return
_inner
def
_wrap_task_call
(
task
f
)
:
    
functools
.
wraps
(
f
)
    
def
_inner
(
*
args
*
*
kwargs
)
:
        
try
:
            
return
f
(
*
args
*
*
kwargs
)
        
except
Exception
:
            
exc_info
=
sys
.
exc_info
(
)
            
with
capture_internal_exceptions
(
)
:
                
_capture_exception
(
task
exc_info
)
            
reraise
(
*
exc_info
)
    
return
_inner
def
_make_event_processor
(
task
uuid
args
kwargs
request
=
None
)
:
    
def
event_processor
(
event
hint
)
:
        
with
capture_internal_exceptions
(
)
:
            
tags
=
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
            
tags
[
"
celery_task_id
"
]
=
uuid
            
extra
=
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
            
extra
[
"
celery
-
job
"
]
=
{
                
"
task_name
"
:
task
.
name
                
"
args
"
:
args
                
"
kwargs
"
:
kwargs
            
}
        
if
"
exc_info
"
in
hint
:
            
with
capture_internal_exceptions
(
)
:
                
if
issubclass
(
hint
[
"
exc_info
"
]
[
0
]
SoftTimeLimitExceeded
)
:
                    
event
[
"
fingerprint
"
]
=
[
                        
"
celery
"
                        
"
SoftTimeLimitExceeded
"
                        
getattr
(
task
"
name
"
task
)
                    
]
        
return
event
    
return
event_processor
def
_capture_exception
(
task
exc_info
)
:
    
hub
=
Hub
.
current
    
if
hub
.
get_integration
(
CeleryIntegration
)
is
None
:
        
return
    
if
isinstance
(
exc_info
[
1
]
CELERY_CONTROL_FLOW_EXCEPTIONS
)
:
        
_set_status
(
hub
"
aborted
"
)
        
return
    
_set_status
(
hub
"
internal_error
"
)
    
if
hasattr
(
task
"
throws
"
)
and
isinstance
(
exc_info
[
1
]
task
.
throws
)
:
        
return
    
client
=
hub
.
client
    
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
        
mechanism
=
{
"
type
"
:
"
celery
"
"
handled
"
:
False
}
    
)
    
hub
.
capture_event
(
event
hint
=
hint
)
def
_set_status
(
hub
status
)
:
    
with
capture_internal_exceptions
(
)
:
        
with
hub
.
configure_scope
(
)
as
scope
:
            
if
scope
.
span
is
not
None
:
                
scope
.
span
.
set_status
(
status
)
def
_patch_worker_exit
(
)
:
    
from
billiard
.
pool
import
Worker
    
old_workloop
=
Worker
.
workloop
    
def
sentry_workloop
(
*
args
*
*
kwargs
)
:
        
try
:
            
return
old_workloop
(
*
args
*
*
kwargs
)
        
finally
:
            
with
capture_internal_exceptions
(
)
:
                
hub
=
Hub
.
current
                
if
hub
.
get_integration
(
CeleryIntegration
)
is
not
None
:
                    
hub
.
flush
(
)
    
Worker
.
workloop
=
sentry_workloop
