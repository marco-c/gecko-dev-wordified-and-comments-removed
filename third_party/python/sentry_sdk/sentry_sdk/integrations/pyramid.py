from
__future__
import
absolute_import
import
os
import
sys
import
weakref
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
scope
import
Scope
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
    
event_from_exception
)
from
sentry_sdk
.
_compat
import
reraise
iteritems
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
try
:
    
from
pyramid
.
httpexceptions
import
HTTPException
    
from
pyramid
.
request
import
Request
except
ImportError
:
    
raise
DidNotEnable
(
"
Pyramid
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
pyramid
.
response
import
Response
    
from
typing
import
Any
    
from
sentry_sdk
.
integrations
.
wsgi
import
_ScopedResponse
    
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
Optional
    
from
webob
.
cookies
import
RequestCookies
    
from
webob
.
compat
import
cgi_FieldStorage
    
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
if
getattr
(
Request
"
authenticated_userid
"
None
)
:
    
def
authenticated_userid
(
request
)
:
        
return
request
.
authenticated_userid
else
:
    
from
pyramid
.
security
import
authenticated_userid
TRANSACTION_STYLE_VALUES
=
(
"
route_name
"
"
route_pattern
"
)
class
PyramidIntegration
(
Integration
)
:
    
identifier
=
"
pyramid
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
route_name
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
        
from
pyramid
import
router
        
old_call_view
=
router
.
_call_view
        
def
sentry_patched_call_view
(
registry
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
            
integration
=
hub
.
get_integration
(
PyramidIntegration
)
            
if
integration
is
not
None
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
                    
_set_transaction_name_and_source
(
                        
scope
integration
.
transaction_style
request
                    
)
                    
scope
.
add_event_processor
(
                        
_make_event_processor
(
weakref
.
ref
(
request
)
integration
)
                    
)
            
return
old_call_view
(
registry
request
*
args
*
*
kwargs
)
        
router
.
_call_view
=
sentry_patched_call_view
        
if
hasattr
(
Request
"
invoke_exception_view
"
)
:
            
old_invoke_exception_view
=
Request
.
invoke_exception_view
            
def
sentry_patched_invoke_exception_view
(
self
*
args
*
*
kwargs
)
:
                
rv
=
old_invoke_exception_view
(
self
*
args
*
*
kwargs
)
                
if
(
                    
self
.
exc_info
                    
and
all
(
self
.
exc_info
)
                    
and
rv
.
status_int
=
=
500
                    
and
Hub
.
current
.
get_integration
(
PyramidIntegration
)
is
not
None
                
)
:
                    
_capture_exception
(
self
.
exc_info
)
                
return
rv
            
Request
.
invoke_exception_view
=
sentry_patched_invoke_exception_view
        
old_wsgi_call
=
router
.
Router
.
__call__
        
def
sentry_patched_wsgi_call
(
self
environ
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
PyramidIntegration
)
            
if
integration
is
None
:
                
return
old_wsgi_call
(
self
environ
start_response
)
            
def
sentry_patched_inner_wsgi_call
(
environ
start_response
)
:
                
try
:
                    
return
old_wsgi_call
(
self
environ
start_response
)
                
except
Exception
:
                    
einfo
=
sys
.
exc_info
(
)
                    
_capture_exception
(
einfo
)
                    
reraise
(
*
einfo
)
            
return
SentryWsgiMiddleware
(
sentry_patched_inner_wsgi_call
)
(
                
environ
start_response
            
)
        
router
.
Router
.
__call__
=
sentry_patched_wsgi_call
def
_capture_exception
(
exc_info
)
:
    
if
exc_info
[
0
]
is
None
or
issubclass
(
exc_info
[
0
]
HTTPException
)
:
        
return
    
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
PyramidIntegration
)
is
None
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
pyramid
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
_set_transaction_name_and_source
(
scope
transaction_style
request
)
:
    
try
:
        
name_for_style
=
{
            
"
route_name
"
:
request
.
matched_route
.
name
            
"
route_pattern
"
:
request
.
matched_route
.
pattern
        
}
        
scope
.
set_transaction_name
(
            
name_for_style
[
transaction_style
]
            
source
=
SOURCE_FOR_STYLE
[
transaction_style
]
        
)
    
except
Exception
:
        
pass
class
PyramidRequestExtractor
(
RequestExtractor
)
:
    
def
url
(
self
)
:
        
return
self
.
request
.
path_url
    
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
environ
    
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
text
    
def
form
(
self
)
:
        
return
{
            
key
:
value
            
for
key
value
in
iteritems
(
self
.
request
.
POST
)
            
if
not
getattr
(
value
"
filename
"
None
)
        
}
    
def
files
(
self
)
:
        
return
{
            
key
:
value
            
for
key
value
in
iteritems
(
self
.
request
.
POST
)
            
if
getattr
(
value
"
filename
"
None
)
        
}
    
def
size_of_file
(
self
postdata
)
:
        
file
=
postdata
.
file
        
try
:
            
return
os
.
fstat
(
file
.
fileno
(
)
)
.
st_size
        
except
Exception
:
            
return
0
def
_make_event_processor
(
weak_request
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
            
PyramidRequestExtractor
(
request
)
.
extract_into_event
(
event
)
        
if
_should_send_default_pii
(
)
:
            
with
capture_internal_exceptions
(
)
:
                
user_info
=
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
                
user_info
.
setdefault
(
"
id
"
authenticated_userid
(
request
)
)
        
return
event
    
return
event_processor
