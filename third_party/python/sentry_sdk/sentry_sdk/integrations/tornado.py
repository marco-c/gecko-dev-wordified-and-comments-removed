import
weakref
import
contextlib
from
inspect
import
iscoroutinefunction
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
hub
import
Hub
_should_send_default_pii
from
sentry_sdk
.
tracing
import
(
    
TRANSACTION_SOURCE_COMPONENT
    
TRANSACTION_SOURCE_ROUTE
)
from
sentry_sdk
.
utils
import
(
    
HAS_REAL_CONTEXTVARS
    
CONTEXTVARS_ERROR_MESSAGE
    
event_from_exception
    
capture_internal_exceptions
    
transaction_from_function
)
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
_wsgi_common
import
(
    
RequestExtractor
    
_filter_headers
    
_is_json_content_type
)
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
_compat
import
iteritems
try
:
    
from
tornado
import
version_info
as
TORNADO_VERSION
    
from
tornado
.
web
import
RequestHandler
HTTPError
    
from
tornado
.
gen
import
coroutine
except
ImportError
:
    
raise
DidNotEnable
(
"
Tornado
not
installed
"
)
from
sentry_sdk
.
_types
import
TYPE_CHECKING
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
Optional
    
from
typing
import
Dict
    
from
typing
import
Callable
    
from
typing
import
Generator
    
from
sentry_sdk
.
_types
import
Event
EventProcessor
class
TornadoIntegration
(
Integration
)
:
    
identifier
=
"
tornado
"
    
staticmethod
    
def
setup_once
(
)
:
        
if
TORNADO_VERSION
<
(
5
0
)
:
            
raise
DidNotEnable
(
"
Tornado
5
+
required
"
)
        
if
not
HAS_REAL_CONTEXTVARS
:
            
raise
DidNotEnable
(
                
"
The
tornado
integration
for
Sentry
requires
Python
3
.
7
+
or
the
aiocontextvars
package
"
                
+
CONTEXTVARS_ERROR_MESSAGE
            
)
        
ignore_logger
(
"
tornado
.
access
"
)
        
old_execute
=
RequestHandler
.
_execute
        
awaitable
=
iscoroutinefunction
(
old_execute
)
        
if
awaitable
:
            
async
def
sentry_execute_request_handler
(
self
*
args
*
*
kwargs
)
:
                
with
_handle_request_impl
(
self
)
:
                    
return
await
old_execute
(
self
*
args
*
*
kwargs
)
        
else
:
            
coroutine
            
def
sentry_execute_request_handler
(
self
*
args
*
*
kwargs
)
:
                
with
_handle_request_impl
(
self
)
:
                    
result
=
yield
from
old_execute
(
self
*
args
*
*
kwargs
)
                    
return
result
        
RequestHandler
.
_execute
=
sentry_execute_request_handler
        
old_log_exception
=
RequestHandler
.
log_exception
        
def
sentry_log_exception
(
self
ty
value
tb
*
args
*
*
kwargs
)
:
            
_capture_exception
(
ty
value
tb
)
            
return
old_log_exception
(
self
ty
value
tb
*
args
*
*
kwargs
)
        
RequestHandler
.
log_exception
=
sentry_log_exception
contextlib
.
contextmanager
def
_handle_request_impl
(
self
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
TornadoIntegration
)
    
if
integration
is
None
:
        
yield
    
weak_handler
=
weakref
.
ref
(
self
)
    
with
Hub
(
hub
)
as
hub
:
        
headers
=
self
.
request
.
headers
        
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
clear_breadcrumbs
(
)
            
processor
=
_make_event_processor
(
weak_handler
)
            
scope
.
add_event_processor
(
processor
)
        
transaction
=
continue_trace
(
            
headers
            
op
=
OP
.
HTTP_SERVER
            
name
=
"
generic
Tornado
request
"
            
source
=
TRANSACTION_SOURCE_ROUTE
        
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
tornado_request
"
:
self
.
request
}
        
)
:
            
yield
def
_capture_exception
(
ty
value
tb
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
TornadoIntegration
)
is
None
:
        
return
    
if
isinstance
(
value
HTTPError
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
        
(
ty
value
tb
)
        
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
tornado
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
_make_event_processor
(
weak_handler
)
:
    
def
tornado_processor
(
event
hint
)
:
        
handler
=
weak_handler
(
)
        
if
handler
is
None
:
            
return
event
        
request
=
handler
.
request
        
with
capture_internal_exceptions
(
)
:
            
method
=
getattr
(
handler
handler
.
request
.
method
.
lower
(
)
)
            
event
[
"
transaction
"
]
=
transaction_from_function
(
method
)
or
"
"
            
event
[
"
transaction_info
"
]
=
{
"
source
"
:
TRANSACTION_SOURCE_COMPONENT
}
        
with
capture_internal_exceptions
(
)
:
            
extractor
=
TornadoRequestExtractor
(
request
)
            
extractor
.
extract_into_event
(
event
)
            
request_info
=
event
[
"
request
"
]
            
request_info
[
"
url
"
]
=
"
%
s
:
/
/
%
s
%
s
"
%
(
                
request
.
protocol
                
request
.
host
                
request
.
path
            
)
            
request_info
[
"
query_string
"
]
=
request
.
query
            
request_info
[
"
method
"
]
=
request
.
method
            
request_info
[
"
env
"
]
=
{
"
REMOTE_ADDR
"
:
request
.
remote_ip
}
            
request_info
[
"
headers
"
]
=
_filter_headers
(
dict
(
request
.
headers
)
)
        
with
capture_internal_exceptions
(
)
:
            
if
handler
.
current_user
and
_should_send_default_pii
(
)
:
                
event
.
setdefault
(
"
user
"
{
}
)
.
setdefault
(
"
is_authenticated
"
True
)
        
return
event
    
return
tornado_processor
class
TornadoRequestExtractor
(
RequestExtractor
)
:
    
def
content_length
(
self
)
:
        
if
self
.
request
.
body
is
None
:
            
return
0
        
return
len
(
self
.
request
.
body
)
    
def
cookies
(
self
)
:
        
return
{
k
:
v
.
value
for
k
v
in
iteritems
(
self
.
request
.
cookies
)
}
    
def
raw_data
(
self
)
:
        
return
self
.
request
.
body
    
def
form
(
self
)
:
        
return
{
            
k
:
[
v
.
decode
(
"
latin1
"
"
replace
"
)
for
v
in
vs
]
            
for
k
vs
in
iteritems
(
self
.
request
.
body_arguments
)
        
}
    
def
is_json
(
self
)
:
        
return
_is_json_content_type
(
self
.
request
.
headers
.
get
(
"
content
-
type
"
)
)
    
def
files
(
self
)
:
        
return
{
k
:
v
[
0
]
for
k
v
in
iteritems
(
self
.
request
.
files
)
if
v
}
    
def
size_of_file
(
self
file
)
:
        
return
len
(
file
.
body
or
(
)
)
