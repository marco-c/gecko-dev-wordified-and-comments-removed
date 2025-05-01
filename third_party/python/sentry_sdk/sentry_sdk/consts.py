from
sentry_sdk
.
_types
import
MYPY
if
MYPY
:
    
import
sentry_sdk
    
from
typing
import
Optional
    
from
typing
import
Callable
    
from
typing
import
Union
    
from
typing
import
List
    
from
typing
import
Type
    
from
typing
import
Dict
    
from
typing
import
Any
    
from
typing
import
Sequence
    
from
typing_extensions
import
TypedDict
    
from
sentry_sdk
.
integrations
import
Integration
    
from
sentry_sdk
.
_types
import
(
        
BreadcrumbProcessor
        
Event
        
EventProcessor
        
TracesSampler
        
TransactionProcessor
    
)
    
Experiments
=
TypedDict
(
        
"
Experiments
"
        
{
            
"
max_spans
"
:
Optional
[
int
]
            
"
record_sql_params
"
:
Optional
[
bool
]
            
"
smart_transaction_trimming
"
:
Optional
[
bool
]
            
"
propagate_tracestate
"
:
Optional
[
bool
]
            
"
custom_measurements
"
:
Optional
[
bool
]
            
"
profiles_sample_rate
"
:
Optional
[
float
]
            
"
profiler_mode
"
:
Optional
[
str
]
        
}
        
total
=
False
    
)
DEFAULT_QUEUE_SIZE
=
100
DEFAULT_MAX_BREADCRUMBS
=
100
SENSITIVE_DATA_SUBSTITUTE
=
"
[
Filtered
]
"
class
INSTRUMENTER
:
    
SENTRY
=
"
sentry
"
    
OTEL
=
"
otel
"
class
OP
:
    
DB
=
"
db
"
    
DB_REDIS
=
"
db
.
redis
"
    
EVENT_DJANGO
=
"
event
.
django
"
    
FUNCTION
=
"
function
"
    
FUNCTION_AWS
=
"
function
.
aws
"
    
FUNCTION_GCP
=
"
function
.
gcp
"
    
HTTP_CLIENT
=
"
http
.
client
"
    
HTTP_CLIENT_STREAM
=
"
http
.
client
.
stream
"
    
HTTP_SERVER
=
"
http
.
server
"
    
MIDDLEWARE_DJANGO
=
"
middleware
.
django
"
    
MIDDLEWARE_STARLETTE
=
"
middleware
.
starlette
"
    
MIDDLEWARE_STARLETTE_RECEIVE
=
"
middleware
.
starlette
.
receive
"
    
MIDDLEWARE_STARLETTE_SEND
=
"
middleware
.
starlette
.
send
"
    
MIDDLEWARE_STARLITE
=
"
middleware
.
starlite
"
    
MIDDLEWARE_STARLITE_RECEIVE
=
"
middleware
.
starlite
.
receive
"
    
MIDDLEWARE_STARLITE_SEND
=
"
middleware
.
starlite
.
send
"
    
QUEUE_SUBMIT_CELERY
=
"
queue
.
submit
.
celery
"
    
QUEUE_TASK_CELERY
=
"
queue
.
task
.
celery
"
    
QUEUE_TASK_RQ
=
"
queue
.
task
.
rq
"
    
SUBPROCESS
=
"
subprocess
"
    
SUBPROCESS_WAIT
=
"
subprocess
.
wait
"
    
SUBPROCESS_COMMUNICATE
=
"
subprocess
.
communicate
"
    
TEMPLATE_RENDER
=
"
template
.
render
"
    
VIEW_RENDER
=
"
view
.
render
"
    
VIEW_RESPONSE_RENDER
=
"
view
.
response
.
render
"
    
WEBSOCKET_SERVER
=
"
websocket
.
server
"
class
ClientConstructor
(
object
)
:
    
def
__init__
(
        
self
        
dsn
=
None
        
with_locals
=
True
        
max_breadcrumbs
=
DEFAULT_MAX_BREADCRUMBS
        
release
=
None
        
environment
=
None
        
server_name
=
None
        
shutdown_timeout
=
2
        
integrations
=
[
]
        
in_app_include
=
[
]
        
in_app_exclude
=
[
]
        
default_integrations
=
True
        
dist
=
None
        
transport
=
None
        
transport_queue_size
=
DEFAULT_QUEUE_SIZE
        
sample_rate
=
1
.
0
        
send_default_pii
=
False
        
http_proxy
=
None
        
https_proxy
=
None
        
ignore_errors
=
[
]
        
request_bodies
=
"
medium
"
        
before_send
=
None
        
before_breadcrumb
=
None
        
debug
=
False
        
attach_stacktrace
=
False
        
ca_certs
=
None
        
propagate_traces
=
True
        
traces_sample_rate
=
None
        
traces_sampler
=
None
        
auto_enabling_integrations
=
True
        
auto_session_tracking
=
True
        
send_client_reports
=
True
        
_experiments
=
{
}
        
proxy_headers
=
None
        
instrumenter
=
INSTRUMENTER
.
SENTRY
        
before_send_transaction
=
None
    
)
:
        
pass
def
_get_default_options
(
)
:
    
import
inspect
    
if
hasattr
(
inspect
"
getfullargspec
"
)
:
        
getargspec
=
inspect
.
getfullargspec
    
else
:
        
getargspec
=
inspect
.
getargspec
    
a
=
getargspec
(
ClientConstructor
.
__init__
)
    
defaults
=
a
.
defaults
or
(
)
    
return
dict
(
zip
(
a
.
args
[
-
len
(
defaults
)
:
]
defaults
)
)
DEFAULT_OPTIONS
=
_get_default_options
(
)
del
_get_default_options
VERSION
=
"
1
.
14
.
0
"
