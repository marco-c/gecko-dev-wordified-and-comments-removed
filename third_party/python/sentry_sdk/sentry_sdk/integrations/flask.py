from
__future__
import
absolute_import
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
utils
import
capture_internal_exceptions
event_from_exception
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
wsgi
import
SentryWsgiMiddleware
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
_types
import
MYPY
if
MYPY
:
    
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
Any
    
from
typing
import
Dict
    
from
werkzeug
.
datastructures
import
ImmutableTypeConversionDict
    
from
werkzeug
.
datastructures
import
ImmutableMultiDict
    
from
werkzeug
.
datastructures
import
FileStorage
    
from
typing
import
Union
    
from
typing
import
Callable
    
from
sentry_sdk
.
_types
import
EventProcessor
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
(
        
Request
        
Flask
        
_request_ctx_stack
        
_app_ctx_stack
        
__version__
as
FLASK_VERSION
    
)
    
from
flask
.
signals
import
(
        
appcontext_pushed
        
appcontext_tearing_down
        
got_request_exception
        
request_started
    
)
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
endpoint
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
FLASK_VERSION
.
split
(
"
.
"
)
[
:
3
]
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
Flask
version
:
{
}
"
.
format
(
FLASK_VERSION
)
)
        
if
version
<
(
0
11
)
:
            
raise
DidNotEnable
(
"
Flask
0
.
11
or
newer
is
required
.
"
)
        
appcontext_pushed
.
connect
(
_push_appctx
)
        
appcontext_tearing_down
.
connect
(
_pop_appctx
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
Hub
.
current
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
            
return
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
)
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
_push_appctx
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
FlaskIntegration
)
is
not
None
:
        
scope_manager
=
hub
.
push_scope
(
)
        
scope_manager
.
__enter__
(
)
        
_app_ctx_stack
.
top
.
sentry_sdk_scope_manager
=
scope_manager
        
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
flask
"
def
_pop_appctx
(
*
args
*
*
kwargs
)
:
    
scope_manager
=
getattr
(
_app_ctx_stack
.
top
"
sentry_sdk_scope_manager
"
None
)
    
if
scope_manager
is
not
None
:
        
scope_manager
.
__exit__
(
None
None
None
)
def
_request_started
(
sender
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
FlaskIntegration
)
    
if
integration
is
None
:
        
return
    
app
=
_app_ctx_stack
.
top
.
app
    
with
hub
.
configure_scope
(
)
as
scope
:
        
request
=
_request_ctx_stack
.
top
.
request
        
try
:
            
if
integration
.
transaction_style
=
=
"
endpoint
"
:
                
scope
.
transaction
=
request
.
url_rule
.
endpoint
            
elif
integration
.
transaction_style
=
=
"
url
"
:
                
scope
.
transaction
=
request
.
url_rule
.
rule
        
except
Exception
:
            
pass
        
weak_request
=
weakref
.
ref
(
request
)
        
evt_processor
=
_make_request_event_processor
(
            
app
weak_request
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
weak_request
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
_should_send_default_pii
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
FlaskIntegration
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
flask
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
            
user_info
.
setdefault
(
"
username
"
user
.
email
)
        
except
Exception
:
            
pass
