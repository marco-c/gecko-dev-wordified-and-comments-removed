import
sys
import
weakref
from
sentry_sdk
.
_compat
import
reraise
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
integrations
.
_wsgi_common
import
(
    
_filter_headers
    
request_body_within_bounds
)
from
sentry_sdk
.
tracing
import
Span
from
sentry_sdk
.
utils
import
(
    
capture_internal_exceptions
    
event_from_exception
    
transaction_from_function
    
HAS_REAL_CONTEXTVARS
    
AnnotatedValue
)
try
:
    
import
asyncio
    
from
aiohttp
import
__version__
as
AIOHTTP_VERSION
    
from
aiohttp
.
web
import
Application
HTTPException
UrlDispatcher
except
ImportError
:
    
raise
DidNotEnable
(
"
AIOHTTP
not
installed
"
)
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
aiohttp
.
web_request
import
Request
    
from
aiohttp
.
abc
import
AbstractMatchInfo
    
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
Optional
    
from
typing
import
Tuple
    
from
typing
import
Callable
    
from
typing
import
Union
    
from
sentry_sdk
.
utils
import
ExcInfo
    
from
sentry_sdk
.
_types
import
EventProcessor
class
AioHttpIntegration
(
Integration
)
:
    
identifier
=
"
aiohttp
"
    
staticmethod
    
def
setup_once
(
)
:
        
try
:
            
version
=
tuple
(
map
(
int
AIOHTTP_VERSION
.
split
(
"
.
"
)
)
)
        
except
(
TypeError
ValueError
)
:
            
raise
DidNotEnable
(
"
AIOHTTP
version
unparseable
:
{
}
"
.
format
(
version
)
)
        
if
version
<
(
3
4
)
:
            
raise
DidNotEnable
(
"
AIOHTTP
3
.
4
or
newer
required
.
"
)
        
if
not
HAS_REAL_CONTEXTVARS
:
            
raise
RuntimeError
(
                
"
The
aiohttp
integration
for
Sentry
requires
Python
3
.
7
+
"
                
"
or
aiocontextvars
package
"
            
)
        
ignore_logger
(
"
aiohttp
.
server
"
)
        
old_handle
=
Application
.
_handle
        
async
def
sentry_app_handle
(
self
request
*
args
*
*
kwargs
)
:
            
async
def
inner
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
AioHttpIntegration
)
is
None
:
                    
return
await
old_handle
(
self
request
*
args
*
*
kwargs
)
                
weak_request
=
weakref
.
ref
(
request
)
                
with
Hub
(
Hub
.
current
)
as
hub
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
                        
scope
.
clear_breadcrumbs
(
)
                        
scope
.
add_event_processor
(
_make_request_processor
(
weak_request
)
)
                    
span
=
Span
.
continue_from_headers
(
request
.
headers
)
                    
span
.
op
=
"
http
.
server
"
                    
span
.
transaction
=
"
generic
AIOHTTP
request
"
                    
with
hub
.
start_span
(
span
)
:
                        
try
:
                            
response
=
await
old_handle
(
self
request
)
                        
except
HTTPException
as
e
:
                            
span
.
set_http_status
(
e
.
status_code
)
                            
raise
                        
except
asyncio
.
CancelledError
:
                            
span
.
set_status
(
"
cancelled
"
)
                            
raise
                        
except
Exception
:
                            
reraise
(
*
_capture_exception
(
hub
)
)
                        
span
.
set_http_status
(
response
.
status
)
                        
return
response
            
return
await
asyncio
.
get_event_loop
(
)
.
create_task
(
inner
(
)
)
        
Application
.
_handle
=
sentry_app_handle
        
old_urldispatcher_resolve
=
UrlDispatcher
.
resolve
        
async
def
sentry_urldispatcher_resolve
(
self
request
)
:
            
rv
=
await
old_urldispatcher_resolve
(
self
request
)
            
name
=
None
            
try
:
                
name
=
transaction_from_function
(
rv
.
handler
)
            
except
Exception
:
                
pass
            
if
name
is
not
None
:
                
with
Hub
.
current
.
configure_scope
(
)
as
scope
:
                    
scope
.
transaction
=
name
            
return
rv
        
UrlDispatcher
.
resolve
=
sentry_urldispatcher_resolve
def
_make_request_processor
(
weak_request
)
:
    
def
aiohttp_processor
(
        
event
        
hint
    
)
:
        
request
=
weak_request
(
)
        
if
request
is
None
:
            
return
event
        
with
capture_internal_exceptions
(
)
:
            
request_info
=
event
.
setdefault
(
"
request
"
{
}
)
            
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
scheme
                
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
query_string
            
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
remote
}
            
hub
=
Hub
.
current
            
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
            
request_info
[
"
data
"
]
=
get_aiohttp_request_data
(
hub
request
)
        
return
event
    
return
aiohttp_processor
def
_capture_exception
(
hub
)
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
hub
.
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
aiohttp
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
    
return
exc_info
BODY_NOT_READ_MESSAGE
=
"
[
Can
'
t
show
request
body
due
to
implementation
details
.
]
"
def
get_aiohttp_request_data
(
hub
request
)
:
    
bytes_body
=
request
.
_read_bytes
    
if
bytes_body
is
not
None
:
        
if
not
request_body_within_bounds
(
hub
.
client
len
(
bytes_body
)
)
:
            
return
AnnotatedValue
(
                
"
"
                
{
"
rem
"
:
[
[
"
!
config
"
"
x
"
0
len
(
bytes_body
)
]
]
"
len
"
:
len
(
bytes_body
)
}
            
)
        
encoding
=
request
.
charset
or
"
utf
-
8
"
        
return
bytes_body
.
decode
(
encoding
"
replace
"
)
    
if
request
.
can_read_body
:
        
return
BODY_NOT_READ_MESSAGE
    
return
None
