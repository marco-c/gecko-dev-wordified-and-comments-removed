import
sentry_sdk
from
sentry_sdk
.
integrations
import
_check_minimum_version
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
from
sentry_sdk
.
integrations
.
wsgi
import
SentryWsgiMiddleware
from
sentry_sdk
.
tracing
import
SOURCE_FOR_STYLE
from
sentry_sdk
.
utils
import
(
    
capture_internal_exceptions
    
ensure_integration_enabled
    
event_from_exception
    
parse_version
)
from
typing
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
Dict
    
from
typing
import
Optional
    
from
sentry_sdk
.
_types
import
Event
EventProcessor
try
:
    
import
falcon
    
from
falcon
import
__version__
as
FALCON_VERSION
except
ImportError
:
    
raise
DidNotEnable
(
"
Falcon
not
installed
"
)
try
:
    
import
falcon
.
app_helpers
    
falcon_helpers
=
falcon
.
app_helpers
    
falcon_app_class
=
falcon
.
App
    
FALCON3
=
True
except
ImportError
:
    
import
falcon
.
api_helpers
    
falcon_helpers
=
falcon
.
api_helpers
    
falcon_app_class
=
falcon
.
API
    
FALCON3
=
False
_FALCON_UNSET
=
None
if
FALCON3
:
    
with
capture_internal_exceptions
(
)
:
        
from
falcon
.
request
import
_UNSET
as
_FALCON_UNSET
class
FalconRequestExtractor
(
RequestExtractor
)
:
    
def
env
(
self
)
:
        
return
self
.
request
.
env
    
def
cookies
(
self
)
:
        
return
self
.
request
.
cookies
    
def
form
(
self
)
:
        
return
None
    
def
files
(
self
)
:
        
return
None
    
def
raw_data
(
self
)
:
        
content_length
=
self
.
content_length
(
)
        
if
content_length
>
0
:
            
return
"
[
REQUEST_CONTAINING_RAW_DATA
]
"
        
else
:
            
return
None
    
def
json
(
self
)
:
        
cached_media
=
None
        
with
capture_internal_exceptions
(
)
:
            
cached_media
=
self
.
request
.
_media
        
if
cached_media
is
not
_FALCON_UNSET
:
            
return
cached_media
        
return
None
class
SentryFalconMiddleware
:
    
"
"
"
Captures
exceptions
in
Falcon
requests
and
send
to
Sentry
"
"
"
    
def
process_request
(
self
req
resp
*
args
*
*
kwargs
)
:
        
integration
=
sentry_sdk
.
get_client
(
)
.
get_integration
(
FalconIntegration
)
        
if
integration
is
None
:
            
return
        
scope
=
sentry_sdk
.
get_isolation_scope
(
)
        
scope
.
_name
=
"
falcon
"
        
scope
.
add_event_processor
(
_make_request_event_processor
(
req
integration
)
)
TRANSACTION_STYLE_VALUES
=
(
"
uri_template
"
"
path
"
)
class
FalconIntegration
(
Integration
)
:
    
identifier
=
"
falcon
"
    
origin
=
f
"
auto
.
http
.
{
identifier
}
"
    
transaction_style
=
"
"
    
def
__init__
(
self
transaction_style
=
"
uri_template
"
)
:
        
if
transaction_style
not
in
TRANSACTION_STYLE_VALUES
:
            
raise
ValueError
(
                
"
Invalid
value
for
transaction_style
:
%
s
(
must
be
in
%
s
)
"
                
%
(
transaction_style
TRANSACTION_STYLE_VALUES
)
            
)
        
self
.
transaction_style
=
transaction_style
    
staticmethod
    
def
setup_once
(
)
:
        
version
=
parse_version
(
FALCON_VERSION
)
        
_check_minimum_version
(
FalconIntegration
version
)
        
_patch_wsgi_app
(
)
        
_patch_handle_exception
(
)
        
_patch_prepare_middleware
(
)
def
_patch_wsgi_app
(
)
:
    
original_wsgi_app
=
falcon_app_class
.
__call__
    
def
sentry_patched_wsgi_app
(
self
env
start_response
)
:
        
integration
=
sentry_sdk
.
get_client
(
)
.
get_integration
(
FalconIntegration
)
        
if
integration
is
None
:
            
return
original_wsgi_app
(
self
env
start_response
)
        
sentry_wrapped
=
SentryWsgiMiddleware
(
            
lambda
envi
start_resp
:
original_wsgi_app
(
self
envi
start_resp
)
            
span_origin
=
FalconIntegration
.
origin
        
)
        
return
sentry_wrapped
(
env
start_response
)
    
falcon_app_class
.
__call__
=
sentry_patched_wsgi_app
def
_patch_handle_exception
(
)
:
    
original_handle_exception
=
falcon_app_class
.
_handle_exception
    
ensure_integration_enabled
(
FalconIntegration
original_handle_exception
)
    
def
sentry_patched_handle_exception
(
self
*
args
)
:
        
ex
=
response
=
None
        
with
capture_internal_exceptions
(
)
:
            
ex
=
next
(
argument
for
argument
in
args
if
isinstance
(
argument
Exception
)
)
            
response
=
next
(
                
argument
for
argument
in
args
if
isinstance
(
argument
falcon
.
Response
)
            
)
        
was_handled
=
original_handle_exception
(
self
*
args
)
        
if
ex
is
None
or
response
is
None
:
            
return
was_handled
        
if
_exception_leads_to_http_5xx
(
ex
response
)
:
            
event
hint
=
event_from_exception
(
                
ex
                
client_options
=
sentry_sdk
.
get_client
(
)
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
falcon
"
"
handled
"
:
False
}
            
)
            
sentry_sdk
.
capture_event
(
event
hint
=
hint
)
        
return
was_handled
    
falcon_app_class
.
_handle_exception
=
sentry_patched_handle_exception
def
_patch_prepare_middleware
(
)
:
    
original_prepare_middleware
=
falcon_helpers
.
prepare_middleware
    
def
sentry_patched_prepare_middleware
(
        
middleware
=
None
independent_middleware
=
False
asgi
=
False
    
)
:
        
if
asgi
:
            
return
original_prepare_middleware
(
middleware
independent_middleware
asgi
)
        
integration
=
sentry_sdk
.
get_client
(
)
.
get_integration
(
FalconIntegration
)
        
if
integration
is
not
None
:
            
middleware
=
[
SentryFalconMiddleware
(
)
]
+
(
middleware
or
[
]
)
        
return
original_prepare_middleware
(
middleware
independent_middleware
)
    
falcon_helpers
.
prepare_middleware
=
sentry_patched_prepare_middleware
def
_exception_leads_to_http_5xx
(
ex
response
)
:
    
is_server_error
=
isinstance
(
ex
falcon
.
HTTPError
)
and
(
ex
.
status
or
"
"
)
.
startswith
(
        
"
5
"
    
)
    
is_unhandled_error
=
not
isinstance
(
        
ex
(
falcon
.
HTTPError
falcon
.
http_status
.
HTTPStatus
)
    
)
    
return
(
is_server_error
or
is_unhandled_error
)
and
(
        
not
FALCON3
or
_has_http_5xx_status
(
response
)
    
)
def
_has_http_5xx_status
(
response
)
:
    
return
response
.
status
.
startswith
(
"
5
"
)
def
_set_transaction_name_and_source
(
event
transaction_style
request
)
:
    
name_for_style
=
{
        
"
uri_template
"
:
request
.
uri_template
        
"
path
"
:
request
.
path
    
}
    
event
[
"
transaction
"
]
=
name_for_style
[
transaction_style
]
    
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
SOURCE_FOR_STYLE
[
transaction_style
]
}
def
_make_request_event_processor
(
req
integration
)
:
    
def
event_processor
(
event
hint
)
:
        
_set_transaction_name_and_source
(
event
integration
.
transaction_style
req
)
        
with
capture_internal_exceptions
(
)
:
            
FalconRequestExtractor
(
req
)
.
extract_into_event
(
event
)
        
return
event
    
return
event_processor
