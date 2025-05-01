from
__future__
import
absolute_import
from
sentry_sdk
.
_types
import
MYPY
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
integrations
import
DidNotEnable
Integration
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
scope
import
Scope
from
sentry_sdk
.
tracing
import
SENTRY_TRACE_HEADER_NAME
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
if
MYPY
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
Markup
Request
    
from
flask
import
__version__
as
FLASK_VERSION
    
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
            
pass
        
else
:
            
if
version
<
(
0
10
)
:
                
raise
DidNotEnable
(
"
Flask
0
.
10
or
newer
is
required
.
"
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
    
sentry_span
=
Hub
.
current
.
scope
.
span
    
context
[
"
sentry_trace
"
]
=
(
        
Markup
(
            
'
<
meta
name
=
"
%
s
"
content
=
"
%
s
"
/
>
'
            
%
(
                
SENTRY_TRACE_HEADER_NAME
                
sentry_span
.
to_traceparent
(
)
            
)
        
)
        
if
sentry_span
        
else
"
"
    
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
flask_request
.
_get_current_object
(
)
        
_set_transaction_name_and_source
(
scope
integration
.
transaction_style
request
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
