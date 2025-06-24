from
__future__
import
absolute_import
import
sys
import
time
try
:
    
from
typing
import
cast
except
ImportError
:
    
cast
=
lambda
_
o
:
o
from
sentry_sdk
.
api
import
continue_trace
from
sentry_sdk
.
consts
import
OP
from
sentry_sdk
.
_compat
import
reraise
from
sentry_sdk
.
_functools
import
wraps
from
sentry_sdk
.
crons
import
capture_checkin
MonitorStatus
from
sentry_sdk
.
hub
import
Hub
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
tracing
import
BAGGAGE_HEADER_NAME
TRANSACTION_SOURCE_TASK
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
    
capture_internal_exceptions
    
event_from_exception
    
logger
    
match_regex_list
)
if
TYPE_CHECKING
:
    
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
Dict
    
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
tracing
import
Span
    
from
sentry_sdk
.
_types
import
(
        
EventProcessor
        
Event
        
Hint
        
ExcInfo
        
MonitorConfig
        
MonitorConfigScheduleType
        
MonitorConfigScheduleUnit
    
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
import
Task
Celery
    
from
celery
.
app
.
trace
import
task_has_custom
    
from
celery
.
beat
import
Scheduler
    
from
celery
.
exceptions
import
(
        
Ignore
        
Reject
        
Retry
        
SoftTimeLimitExceeded
    
)
    
from
celery
.
schedules
import
crontab
schedule
    
from
celery
.
signals
import
(
        
task_failure
        
task_success
        
task_retry
    
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
try
:
    
from
redbeat
.
schedulers
import
RedBeatScheduler
except
ImportError
:
    
RedBeatScheduler
=
None
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
        
monitor_beat_tasks
=
False
        
exclude_beat_tasks
=
None
    
)
:
        
self
.
propagate_traces
=
propagate_traces
        
self
.
monitor_beat_tasks
=
monitor_beat_tasks
        
self
.
exclude_beat_tasks
=
exclude_beat_tasks
        
if
monitor_beat_tasks
:
            
_patch_beat_apply_entry
(
)
            
_patch_redbeat_maybe_due
(
)
            
_setup_celery_beat_signals
(
)
    
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
                
if
task_has_custom
(
task
"
__call__
"
)
:
                    
type
(
task
)
.
__call__
=
_wrap_task_call
(
task
type
(
task
)
.
__call__
)
                
else
:
                    
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
        
from
celery
.
app
.
task
import
Task
        
Task
.
apply_async
=
_wrap_apply_async
(
Task
.
apply_async
)
        
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
_now_seconds_since_epoch
(
)
:
    
return
time
.
time
(
)
class
NoOpMgr
:
    
def
__enter__
(
self
)
:
        
return
None
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
        
return
None
def
_wrap_apply_async
(
f
)
:
    
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
        
kwarg_headers
=
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
        
propagate_traces
=
kwarg_headers
.
pop
(
            
"
sentry
-
propagate
-
traces
"
integration
.
propagate_traces
        
)
        
if
not
propagate_traces
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
        
try
:
            
task_started_from_beat
=
args
[
1
]
[
0
]
=
=
"
BEAT
"
        
except
(
IndexError
TypeError
)
:
            
task_started_from_beat
=
False
        
task
=
args
[
0
]
        
span_mgr
=
(
            
hub
.
start_span
(
op
=
OP
.
QUEUE_SUBMIT_CELERY
description
=
task
.
name
)
            
if
not
task_started_from_beat
            
else
NoOpMgr
(
)
        
)
        
with
span_mgr
as
span
:
            
with
capture_internal_exceptions
(
)
:
                
headers
=
(
                    
dict
(
hub
.
iter_trace_propagation_headers
(
span
)
)
                    
if
span
is
not
None
                    
else
{
}
                
)
                
if
integration
.
monitor_beat_tasks
:
                    
headers
.
update
(
                        
{
                            
"
sentry
-
monitor
-
start
-
timestamp
-
s
"
:
"
%
.
9f
"
                            
%
_now_seconds_since_epoch
(
)
                        
}
                    
)
                
if
headers
:
                    
existing_baggage
=
kwarg_headers
.
get
(
BAGGAGE_HEADER_NAME
)
                    
sentry_baggage
=
headers
.
get
(
BAGGAGE_HEADER_NAME
)
                    
combined_baggage
=
sentry_baggage
or
existing_baggage
                    
if
sentry_baggage
and
existing_baggage
:
                        
combined_baggage
=
"
{
}
{
}
"
.
format
(
                            
existing_baggage
                            
sentry_baggage
                        
)
                    
kwarg_headers
.
update
(
headers
)
                    
if
combined_baggage
:
                        
kwarg_headers
[
BAGGAGE_HEADER_NAME
]
=
combined_baggage
                    
kwarg_headers
.
setdefault
(
"
headers
"
{
}
)
.
update
(
headers
)
                    
if
combined_baggage
:
                        
kwarg_headers
[
"
headers
"
]
[
BAGGAGE_HEADER_NAME
]
=
combined_baggage
                    
for
key
value
in
kwarg_headers
.
items
(
)
:
                        
if
key
.
startswith
(
"
sentry
-
"
)
:
                            
kwarg_headers
[
"
headers
"
]
[
key
]
=
value
                    
kwargs
[
"
headers
"
]
=
kwarg_headers
            
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
            
transaction
=
None
            
with
capture_internal_exceptions
(
)
:
                
transaction
=
continue_trace
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
                    
op
=
OP
.
QUEUE_TASK_CELERY
                    
name
=
"
unknown
celery
task
"
                    
source
=
TRANSACTION_SOURCE_TASK
                
)
                
transaction
.
name
=
task
.
name
                
transaction
.
set_status
(
"
ok
"
)
            
if
transaction
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
start_transaction
(
                
transaction
                
custom_sampling_context
=
{
                    
"
celery_job
"
:
{
                        
"
task
"
:
task
.
name
                        
"
args
"
:
list
(
args
[
1
]
)
                        
"
kwargs
"
:
args
[
2
]
                    
}
                
}
            
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
def
_get_headers
(
task
)
:
    
headers
=
task
.
request
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
    
if
"
headers
"
in
headers
:
        
headers
.
update
(
headers
[
"
headers
"
]
)
        
del
headers
[
"
headers
"
]
    
headers
.
update
(
task
.
request
.
get
(
"
properties
"
)
or
{
}
)
    
return
headers
def
_get_humanized_interval
(
seconds
)
:
    
TIME_UNITS
=
(
        
(
"
day
"
60
*
60
*
24
.
0
)
        
(
"
hour
"
60
*
60
.
0
)
        
(
"
minute
"
60
.
0
)
    
)
    
seconds
=
float
(
seconds
)
    
for
unit
divider
in
TIME_UNITS
:
        
if
seconds
>
=
divider
:
            
interval
=
int
(
seconds
/
divider
)
            
return
(
interval
cast
(
"
MonitorConfigScheduleUnit
"
unit
)
)
    
return
(
int
(
seconds
)
"
second
"
)
def
_get_monitor_config
(
celery_schedule
app
monitor_name
)
:
    
monitor_config
=
{
}
    
schedule_type
=
None
    
schedule_value
=
None
    
schedule_unit
=
None
    
if
isinstance
(
celery_schedule
crontab
)
:
        
schedule_type
=
"
crontab
"
        
schedule_value
=
(
            
"
{
0
.
_orig_minute
}
"
            
"
{
0
.
_orig_hour
}
"
            
"
{
0
.
_orig_day_of_month
}
"
            
"
{
0
.
_orig_month_of_year
}
"
            
"
{
0
.
_orig_day_of_week
}
"
.
format
(
celery_schedule
)
        
)
    
elif
isinstance
(
celery_schedule
schedule
)
:
        
schedule_type
=
"
interval
"
        
(
schedule_value
schedule_unit
)
=
_get_humanized_interval
(
            
celery_schedule
.
seconds
        
)
        
if
schedule_unit
=
=
"
second
"
:
            
logger
.
warning
(
                
"
Intervals
shorter
than
one
minute
are
not
supported
by
Sentry
Crons
.
Monitor
'
%
s
'
has
an
interval
of
%
s
seconds
.
Use
the
exclude_beat_tasks
option
in
the
celery
integration
to
exclude
it
.
"
                
monitor_name
                
schedule_value
            
)
            
return
{
}
    
else
:
        
logger
.
warning
(
            
"
Celery
schedule
type
'
%
s
'
not
supported
by
Sentry
Crons
.
"
            
type
(
celery_schedule
)
        
)
        
return
{
}
    
monitor_config
[
"
schedule
"
]
=
{
}
    
monitor_config
[
"
schedule
"
]
[
"
type
"
]
=
schedule_type
    
monitor_config
[
"
schedule
"
]
[
"
value
"
]
=
schedule_value
    
if
schedule_unit
is
not
None
:
        
monitor_config
[
"
schedule
"
]
[
"
unit
"
]
=
schedule_unit
    
monitor_config
[
"
timezone
"
]
=
(
        
(
            
hasattr
(
celery_schedule
"
tz
"
)
            
and
celery_schedule
.
tz
is
not
None
            
and
str
(
celery_schedule
.
tz
)
        
)
        
or
app
.
timezone
        
or
"
UTC
"
    
)
    
return
monitor_config
def
_patch_beat_apply_entry
(
)
:
    
original_apply_entry
=
Scheduler
.
apply_entry
    
def
sentry_apply_entry
(
*
args
*
*
kwargs
)
:
        
scheduler
schedule_entry
=
args
        
app
=
scheduler
.
app
        
celery_schedule
=
schedule_entry
.
schedule
        
monitor_name
=
schedule_entry
.
name
        
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
None
:
            
return
original_apply_entry
(
*
args
*
*
kwargs
)
        
if
match_regex_list
(
monitor_name
integration
.
exclude_beat_tasks
)
:
            
return
original_apply_entry
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
configure_scope
(
)
as
scope
:
            
scope
.
set_new_propagation_context
(
)
            
monitor_config
=
_get_monitor_config
(
celery_schedule
app
monitor_name
)
            
is_supported_schedule
=
bool
(
monitor_config
)
            
if
is_supported_schedule
:
                
headers
=
schedule_entry
.
options
.
pop
(
"
headers
"
{
}
)
                
headers
.
update
(
                    
{
                        
"
sentry
-
monitor
-
slug
"
:
monitor_name
                        
"
sentry
-
monitor
-
config
"
:
monitor_config
                    
}
                
)
                
check_in_id
=
capture_checkin
(
                    
monitor_slug
=
monitor_name
                    
monitor_config
=
monitor_config
                    
status
=
MonitorStatus
.
IN_PROGRESS
                
)
                
headers
.
update
(
{
"
sentry
-
monitor
-
check
-
in
-
id
"
:
check_in_id
}
)
                
schedule_entry
.
options
[
"
headers
"
]
=
headers
            
return
original_apply_entry
(
*
args
*
*
kwargs
)
    
Scheduler
.
apply_entry
=
sentry_apply_entry
def
_patch_redbeat_maybe_due
(
)
:
    
if
RedBeatScheduler
is
None
:
        
return
    
original_maybe_due
=
RedBeatScheduler
.
maybe_due
    
def
sentry_maybe_due
(
*
args
*
*
kwargs
)
:
        
scheduler
schedule_entry
=
args
        
app
=
scheduler
.
app
        
celery_schedule
=
schedule_entry
.
schedule
        
monitor_name
=
schedule_entry
.
name
        
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
None
:
            
return
original_maybe_due
(
*
args
*
*
kwargs
)
        
if
match_regex_list
(
monitor_name
integration
.
exclude_beat_tasks
)
:
            
return
original_maybe_due
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
configure_scope
(
)
as
scope
:
            
scope
.
set_new_propagation_context
(
)
            
monitor_config
=
_get_monitor_config
(
celery_schedule
app
monitor_name
)
            
is_supported_schedule
=
bool
(
monitor_config
)
            
if
is_supported_schedule
:
                
headers
=
schedule_entry
.
options
.
pop
(
"
headers
"
{
}
)
                
headers
.
update
(
                    
{
                        
"
sentry
-
monitor
-
slug
"
:
monitor_name
                        
"
sentry
-
monitor
-
config
"
:
monitor_config
                    
}
                
)
                
check_in_id
=
capture_checkin
(
                    
monitor_slug
=
monitor_name
                    
monitor_config
=
monitor_config
                    
status
=
MonitorStatus
.
IN_PROGRESS
                
)
                
headers
.
update
(
{
"
sentry
-
monitor
-
check
-
in
-
id
"
:
check_in_id
}
)
                
schedule_entry
.
options
[
"
headers
"
]
=
headers
            
return
original_maybe_due
(
*
args
*
*
kwargs
)
    
RedBeatScheduler
.
maybe_due
=
sentry_maybe_due
def
_setup_celery_beat_signals
(
)
:
    
task_success
.
connect
(
crons_task_success
)
    
task_failure
.
connect
(
crons_task_failure
)
    
task_retry
.
connect
(
crons_task_retry
)
def
crons_task_success
(
sender
*
*
kwargs
)
:
    
logger
.
debug
(
"
celery_task_success
%
s
"
sender
)
    
headers
=
_get_headers
(
sender
)
    
if
"
sentry
-
monitor
-
slug
"
not
in
headers
:
        
return
    
monitor_config
=
headers
.
get
(
"
sentry
-
monitor
-
config
"
{
}
)
    
start_timestamp_s
=
float
(
headers
[
"
sentry
-
monitor
-
start
-
timestamp
-
s
"
]
)
    
capture_checkin
(
        
monitor_slug
=
headers
[
"
sentry
-
monitor
-
slug
"
]
        
monitor_config
=
monitor_config
        
check_in_id
=
headers
[
"
sentry
-
monitor
-
check
-
in
-
id
"
]
        
duration
=
_now_seconds_since_epoch
(
)
-
start_timestamp_s
        
status
=
MonitorStatus
.
OK
    
)
def
crons_task_failure
(
sender
*
*
kwargs
)
:
    
logger
.
debug
(
"
celery_task_failure
%
s
"
sender
)
    
headers
=
_get_headers
(
sender
)
    
if
"
sentry
-
monitor
-
slug
"
not
in
headers
:
        
return
    
monitor_config
=
headers
.
get
(
"
sentry
-
monitor
-
config
"
{
}
)
    
start_timestamp_s
=
float
(
headers
[
"
sentry
-
monitor
-
start
-
timestamp
-
s
"
]
)
    
capture_checkin
(
        
monitor_slug
=
headers
[
"
sentry
-
monitor
-
slug
"
]
        
monitor_config
=
monitor_config
        
check_in_id
=
headers
[
"
sentry
-
monitor
-
check
-
in
-
id
"
]
        
duration
=
_now_seconds_since_epoch
(
)
-
start_timestamp_s
        
status
=
MonitorStatus
.
ERROR
    
)
def
crons_task_retry
(
sender
*
*
kwargs
)
:
    
logger
.
debug
(
"
celery_task_retry
%
s
"
sender
)
    
headers
=
_get_headers
(
sender
)
    
if
"
sentry
-
monitor
-
slug
"
not
in
headers
:
        
return
    
monitor_config
=
headers
.
get
(
"
sentry
-
monitor
-
config
"
{
}
)
    
start_timestamp_s
=
float
(
headers
[
"
sentry
-
monitor
-
start
-
timestamp
-
s
"
]
)
    
capture_checkin
(
        
monitor_slug
=
headers
[
"
sentry
-
monitor
-
slug
"
]
        
monitor_config
=
monitor_config
        
check_in_id
=
headers
[
"
sentry
-
monitor
-
check
-
in
-
id
"
]
        
duration
=
_now_seconds_since_epoch
(
)
-
start_timestamp_s
        
status
=
MonitorStatus
.
ERROR
    
)
