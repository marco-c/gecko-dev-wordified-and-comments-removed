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
utils
import
(
    
capture_internal_exceptions
    
event_from_exception
    
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
typing
import
Callable
    
from
typing
import
Optional
    
from
bottle
import
FileUpload
FormsDict
LocalRequest
    
from
sentry_sdk
.
_types
import
EventProcessor
try
:
    
from
bottle
import
(
        
Bottle
        
Route
        
request
as
bottle_request
        
HTTPResponse
        
__version__
as
BOTTLE_VERSION
    
)
except
ImportError
:
    
raise
DidNotEnable
(
"
Bottle
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
BottleIntegration
(
Integration
)
:
    
identifier
=
"
bottle
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
BOTTLE_VERSION
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
Unparseable
Bottle
version
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
0
12
)
:
            
raise
DidNotEnable
(
"
Bottle
0
.
12
or
newer
required
.
"
)
        
old_app
=
Bottle
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
BottleIntegration
)
            
if
integration
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
        
Bottle
.
__call__
=
sentry_patched_wsgi_app
        
old_handle
=
Bottle
.
_handle
        
def
_patched_handle
(
self
environ
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
BottleIntegration
)
            
if
integration
is
None
:
                
return
old_handle
(
self
environ
)
            
scope_manager
=
hub
.
push_scope
(
)
            
with
scope_manager
:
                
app
=
self
                
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
bottle
"
                    
scope
.
add_event_processor
(
                        
_make_request_event_processor
(
app
bottle_request
integration
)
                    
)
                
res
=
old_handle
(
self
environ
)
            
return
res
        
Bottle
.
_handle
=
_patched_handle
        
old_make_callback
=
Route
.
_make_callback
        
def
patched_make_callback
(
self
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
BottleIntegration
)
            
prepared_callback
=
old_make_callback
(
self
*
args
*
*
kwargs
)
            
if
integration
is
None
:
                
return
prepared_callback
            
client
=
hub
.
client
            
def
wrapped_callback
(
*
args
*
*
kwargs
)
:
                
try
:
                    
res
=
prepared_callback
(
*
args
*
*
kwargs
)
                
except
HTTPResponse
:
                    
raise
                
except
Exception
as
exception
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
bottle
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
                    
raise
exception
                
return
res
            
return
wrapped_callback
        
Route
.
_make_callback
=
patched_make_callback
class
BottleRequestExtractor
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
body
.
read
(
)
    
def
form
(
self
)
:
        
if
self
.
is_json
(
)
:
            
return
None
        
return
self
.
request
.
forms
.
decode
(
)
    
def
files
(
self
)
:
        
if
self
.
is_json
(
)
:
            
return
None
        
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
                
event
[
"
transaction
"
]
=
request
.
route
.
name
or
transaction_from_function
(
                    
request
.
route
.
callback
                
)
            
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
                
event
[
"
transaction
"
]
=
request
.
route
.
rule
        
except
Exception
:
            
pass
        
with
capture_internal_exceptions
(
)
:
            
BottleRequestExtractor
(
request
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
