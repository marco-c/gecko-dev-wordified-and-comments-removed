import
sys
import
weakref
from
inspect
import
isawaitable
from
sentry_sdk
.
_compat
import
urlparse
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
tracing
import
TRANSACTION_SOURCE_COMPONENT
from
sentry_sdk
.
utils
import
(
    
capture_internal_exceptions
    
event_from_exception
    
HAS_REAL_CONTEXTVARS
    
CONTEXTVARS_ERROR_MESSAGE
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
RequestExtractor
_filter_headers
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
Callable
    
from
typing
import
Optional
    
from
typing
import
Union
    
from
typing
import
Tuple
    
from
typing
import
Dict
    
from
sanic
.
request
import
Request
RequestParameters
    
from
sentry_sdk
.
_types
import
Event
EventProcessor
Hint
    
from
sanic
.
router
import
Route
try
:
    
from
sanic
import
Sanic
__version__
as
SANIC_VERSION
    
from
sanic
.
exceptions
import
SanicException
    
from
sanic
.
router
import
Router
    
from
sanic
.
handlers
import
ErrorHandler
except
ImportError
:
    
raise
DidNotEnable
(
"
Sanic
not
installed
"
)
old_error_handler_lookup
=
ErrorHandler
.
lookup
old_handle_request
=
Sanic
.
handle_request
old_router_get
=
Router
.
get
try
:
    
old_startup
=
Sanic
.
_startup
except
AttributeError
:
    
pass
class
SanicIntegration
(
Integration
)
:
    
identifier
=
"
sanic
"
    
version
=
(
0
0
)
    
staticmethod
    
def
setup_once
(
)
:
        
try
:
            
SanicIntegration
.
version
=
tuple
(
map
(
int
SANIC_VERSION
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
Unparsable
Sanic
version
:
{
}
"
.
format
(
SANIC_VERSION
)
)
        
if
SanicIntegration
.
version
<
(
0
8
)
:
            
raise
DidNotEnable
(
"
Sanic
0
.
8
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
DidNotEnable
(
                
"
The
sanic
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
the
aiocontextvars
package
.
"
+
CONTEXTVARS_ERROR_MESSAGE
            
)
        
if
SANIC_VERSION
.
startswith
(
"
0
.
8
.
"
)
:
            
ignore_logger
(
"
root
"
)
        
if
SanicIntegration
.
version
<
(
21
9
)
:
            
_setup_legacy_sanic
(
)
            
return
        
_setup_sanic
(
)
class
SanicRequestExtractor
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
dict
(
self
.
request
.
cookies
)
    
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
self
.
request
.
form
    
def
is_json
(
self
)
:
        
raise
NotImplementedError
(
)
    
def
json
(
self
)
:
        
return
self
.
request
.
json
    
def
files
(
self
)
:
        
return
self
.
request
.
files
    
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
def
_setup_sanic
(
)
:
    
Sanic
.
_startup
=
_startup
    
ErrorHandler
.
lookup
=
_sentry_error_handler_lookup
def
_setup_legacy_sanic
(
)
:
    
Sanic
.
handle_request
=
_legacy_handle_request
    
Router
.
get
=
_legacy_router_get
    
ErrorHandler
.
lookup
=
_sentry_error_handler_lookup
async
def
_startup
(
self
)
:
    
self
.
signal
(
"
http
.
lifecycle
.
request
"
)
(
_hub_enter
)
    
self
.
signal
(
"
http
.
lifecycle
.
response
"
)
(
_hub_exit
)
    
self
.
signal
(
"
http
.
routing
.
after
"
)
(
_set_transaction
)
    
await
old_startup
(
self
)
async
def
_hub_enter
(
request
)
:
    
hub
=
Hub
.
current
    
request
.
ctx
.
_sentry_do_integration
=
(
        
hub
.
get_integration
(
SanicIntegration
)
is
not
None
    
)
    
if
not
request
.
ctx
.
_sentry_do_integration
:
        
return
    
weak_request
=
weakref
.
ref
(
request
)
    
request
.
ctx
.
_sentry_hub
=
Hub
(
hub
)
    
request
.
ctx
.
_sentry_hub
.
__enter__
(
)
    
with
request
.
ctx
.
_sentry_hub
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
async
def
_hub_exit
(
request
*
*
_
)
:
    
request
.
ctx
.
_sentry_hub
.
__exit__
(
None
None
None
)
async
def
_set_transaction
(
request
route
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
SanicIntegration
)
is
not
None
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
                
route_name
=
route
.
name
.
replace
(
request
.
app
.
name
"
"
)
.
strip
(
"
.
"
)
                
scope
.
set_transaction_name
(
                    
route_name
source
=
TRANSACTION_SOURCE_COMPONENT
                
)
def
_sentry_error_handler_lookup
(
self
exception
*
args
*
*
kwargs
)
:
    
_capture_exception
(
exception
)
    
old_error_handler
=
old_error_handler_lookup
(
self
exception
*
args
*
*
kwargs
)
    
if
old_error_handler
is
None
:
        
return
None
    
if
Hub
.
current
.
get_integration
(
SanicIntegration
)
is
None
:
        
return
old_error_handler
    
async
def
sentry_wrapped_error_handler
(
request
exception
)
:
        
try
:
            
response
=
old_error_handler
(
request
exception
)
            
if
isawaitable
(
response
)
:
                
response
=
await
response
            
return
response
        
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
            
_capture_exception
(
exc_info
)
            
reraise
(
*
exc_info
)
        
finally
:
            
if
SanicIntegration
.
version
=
=
(
21
9
)
:
                
await
_hub_exit
(
request
)
    
return
sentry_wrapped_error_handler
async
def
_legacy_handle_request
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
SanicIntegration
)
is
None
:
        
return
old_handle_request
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
hub
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
        
response
=
old_handle_request
(
self
request
*
args
*
*
kwargs
)
        
if
isawaitable
(
response
)
:
            
response
=
await
response
        
return
response
def
_legacy_router_get
(
self
*
args
)
:
    
rv
=
old_router_get
(
self
*
args
)
    
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
SanicIntegration
)
is
not
None
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
SanicIntegration
.
version
and
SanicIntegration
.
version
>
=
(
21
3
)
:
                    
sanic_app_name
=
self
.
ctx
.
app
.
name
                    
sanic_route
=
rv
[
0
]
.
name
                    
if
sanic_route
.
startswith
(
"
%
s
.
"
%
sanic_app_name
)
:
                        
sanic_route
=
sanic_route
[
len
(
sanic_app_name
)
+
1
:
]
                    
scope
.
set_transaction_name
(
                        
sanic_route
source
=
TRANSACTION_SOURCE_COMPONENT
                    
)
                
else
:
                    
scope
.
set_transaction_name
(
                        
rv
[
0
]
.
__name__
source
=
TRANSACTION_SOURCE_COMPONENT
                    
)
    
return
rv
def
_capture_exception
(
exception
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
SanicIntegration
)
    
if
integration
is
None
:
        
return
    
client
=
hub
.
client
    
with
capture_internal_exceptions
(
)
:
        
event
hint
=
event_from_exception
(
            
exception
            
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
sanic
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
_make_request_processor
(
weak_request
)
:
    
def
sanic_processor
(
event
hint
)
:
        
try
:
            
if
hint
and
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
SanicException
)
:
                
return
None
        
except
KeyError
:
            
pass
        
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
            
extractor
=
SanicRequestExtractor
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
            
urlparts
=
urlparse
.
urlsplit
(
request
.
url
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
                
urlparts
.
scheme
                
urlparts
.
netloc
                
urlparts
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
urlparts
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
remote_addr
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
        
return
event
    
return
sanic_processor
