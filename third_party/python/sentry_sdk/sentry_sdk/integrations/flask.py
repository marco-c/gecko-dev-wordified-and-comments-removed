import
sentry_sdk
from
sentry_sdk
.
integrations
import
_check_minimum_version
DidNotEnable
Integration
from
sentry_sdk
.
integrations
.
_wsgi_common
import
(
    
DEFAULT_HTTP_METHODS_TO_CAPTURE
    
RequestExtractor
)
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
scope
import
should_send_default_pii
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
    
package_version
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
Callable
Dict
Union
    
from
sentry_sdk
.
_types
import
Event
EventProcessor
    
from
sentry_sdk
.
integrations
.
wsgi
import
_ScopedResponse
    
from
werkzeug
.
datastructures
import
FileStorage
ImmutableMultiDict
try
:
    
import
flask_login
except
ImportError
:
    
flask_login
=
None
try
:
    
from
flask
import
Flask
Request
    
from
flask
import
request
as
flask_request
    
from
flask
.
signals
import
(
        
before_render_template
        
got_request_exception
        
request_started
    
)
    
from
markupsafe
import
Markup
except
ImportError
:
    
raise
DidNotEnable
(
"
Flask
is
not
installed
"
)
try
:
    
import
blinker
except
ImportError
:
    
raise
DidNotEnable
(
"
blinker
is
not
installed
"
)
TRANSACTION_STYLE_VALUES
=
(
"
endpoint
"
"
url
"
)
class
FlaskIntegration
(
Integration
)
:
    
identifier
=
"
flask
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
endpoint
"
        
http_methods_to_capture
=
DEFAULT_HTTP_METHODS_TO_CAPTURE
    
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
        
self
.
http_methods_to_capture
=
tuple
(
map
(
str
.
upper
http_methods_to_capture
)
)
    
staticmethod
    
def
setup_once
(
)
:
        
try
:
            
from
quart
import
Quart
            
if
Flask
=
=
Quart
:
                
raise
DidNotEnable
(
                    
"
This
is
not
a
Flask
app
but
rather
Quart
pretending
to
be
Flask
"
                
)
        
except
ImportError
:
            
pass
        
version
=
package_version
(
"
flask
"
)
        
_check_minimum_version
(
FlaskIntegration
version
)
        
before_render_template
.
connect
(
_add_sentry_trace
)
        
request_started
.
connect
(
_request_started
)
        
got_request_exception
.
connect
(
_capture_exception
)
        
old_app
=
Flask
.
__call__
        
def
sentry_patched_wsgi_app
(
self
environ
start_response
)
:
            
if
sentry_sdk
.
get_client
(
)
.
get_integration
(
FlaskIntegration
)
is
None
:
                
return
old_app
(
self
environ
start_response
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
FlaskIntegration
)
            
middleware
=
SentryWsgiMiddleware
(
                
lambda
*
a
*
*
kw
:
old_app
(
self
*
a
*
*
kw
)
                
span_origin
=
FlaskIntegration
.
origin
                
http_methods_to_capture
=
(
                    
integration
.
http_methods_to_capture
                    
if
integration
                    
else
DEFAULT_HTTP_METHODS_TO_CAPTURE
                
)
            
)
            
return
middleware
(
environ
start_response
)
        
Flask
.
__call__
=
sentry_patched_wsgi_app
def
_add_sentry_trace
(
sender
template
context
*
*
extra
)
:
    
if
"
sentry_trace
"
in
context
:
        
return
    
scope
=
sentry_sdk
.
get_current_scope
(
)
    
trace_meta
=
Markup
(
scope
.
trace_propagation_meta
(
)
)
    
context
[
"
sentry_trace
"
]
=
trace_meta
    
context
[
"
sentry_trace_meta
"
]
=
trace_meta
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
url
"
:
request
.
url_rule
.
rule
            
"
endpoint
"
:
request
.
url_rule
.
endpoint
        
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
def
_request_started
(
app
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
FlaskIntegration
)
    
if
integration
is
None
:
        
return
    
request
=
flask_request
.
_get_current_object
(
)
    
_set_transaction_name_and_source
(
        
sentry_sdk
.
get_current_scope
(
)
integration
.
transaction_style
request
    
)
    
scope
=
sentry_sdk
.
get_isolation_scope
(
)
    
evt_processor
=
_make_request_event_processor
(
app
request
integration
)
    
scope
.
add_event_processor
(
evt_processor
)
class
FlaskRequestExtractor
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
environ
    
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
[
0
]
if
isinstance
(
v
list
)
and
len
(
v
)
=
=
1
else
v
            
for
k
v
in
self
.
request
.
cookies
.
items
(
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
get_data
(
)
    
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
is_json
(
self
)
:
        
return
self
.
request
.
is_json
    
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
get_json
(
silent
=
True
)
    
def
size_of_file
(
self
file
)
:
        
return
file
.
content_length
def
_make_request_event_processor
(
app
request
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
            
FlaskRequestExtractor
(
request
)
.
extract_into_event
(
event
)
        
if
should_send_default_pii
(
)
:
            
with
capture_internal_exceptions
(
)
:
                
_add_user_to_event
(
event
)
        
return
event
    
return
inner
ensure_integration_enabled
(
FlaskIntegration
)
def
_capture_exception
(
sender
exception
*
*
kwargs
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
flask
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
def
_add_user_to_event
(
event
)
:
    
if
flask_login
is
None
:
        
return
    
user
=
flask_login
.
current_user
    
if
user
is
None
:
        
return
    
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
        
try
:
            
user_info
.
setdefault
(
"
id
"
user
.
get_id
(
)
)
        
except
AttributeError
:
            
pass
        
try
:
            
user_info
.
setdefault
(
"
email
"
user
.
email
)
        
except
Exception
:
            
pass
        
try
:
            
user_info
.
setdefault
(
"
username
"
user
.
username
)
        
except
Exception
:
            
pass
