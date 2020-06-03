from
__future__
import
absolute_import
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
utils
import
capture_internal_exceptions
event_from_exception
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
EventProcessor
try
:
    
import
falcon
    
import
falcon
.
api_helpers
    
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
        
try
:
            
return
self
.
request
.
media
        
except
falcon
.
errors
.
HTTPBadRequest
:
            
return
self
.
request
.
_media
class
SentryFalconMiddleware
(
object
)
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
FalconIntegration
)
        
if
integration
is
None
:
            
return
        
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
    
transaction_style
=
None
    
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
        
try
:
            
version
=
tuple
(
map
(
int
FALCON_VERSION
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
ValueError
TypeError
)
:
            
raise
DidNotEnable
(
"
Unparseable
Falcon
version
:
{
}
"
.
format
(
FALCON_VERSION
)
)
        
if
version
<
(
1
4
)
:
            
raise
DidNotEnable
(
"
Falcon
1
.
4
or
newer
required
.
"
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
falcon
.
API
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
        
)
        
return
sentry_wrapped
(
env
start_response
)
    
falcon
.
API
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
falcon
.
API
.
_handle_exception
    
def
sentry_patched_handle_exception
(
self
*
args
)
:
        
if
isinstance
(
args
[
0
]
Exception
)
:
            
ex
=
args
[
0
]
        
else
:
            
ex
=
args
[
2
]
        
was_handled
=
original_handle_exception
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
        
integration
=
hub
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
and
not
_is_falcon_http_error
(
ex
)
:
            
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
                
ex
                
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
falcon
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
was_handled
    
falcon
.
API
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
falcon
.
api_helpers
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
    
falcon
.
api_helpers
.
prepare_middleware
=
sentry_patched_prepare_middleware
def
_is_falcon_http_error
(
ex
)
:
    
return
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
def
_make_request_event_processor
(
req
integration
)
:
    
def
inner
(
event
hint
)
:
        
if
integration
.
transaction_style
=
=
"
uri_template
"
:
            
event
[
"
transaction
"
]
=
req
.
uri_template
        
elif
integration
.
transaction_style
=
=
"
path
"
:
            
event
[
"
transaction
"
]
=
req
.
path
        
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
inner
