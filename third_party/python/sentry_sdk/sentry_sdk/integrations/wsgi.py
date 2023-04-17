import
functools
import
sys
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
(
    
ContextVar
    
capture_internal_exceptions
    
event_from_exception
)
from
sentry_sdk
.
_compat
import
PY2
reraise
iteritems
from
sentry_sdk
.
tracing
import
Span
from
sentry_sdk
.
sessions
import
auto_session_tracking
from
sentry_sdk
.
integrations
.
_wsgi_common
import
_filter_headers
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
Callable
    
from
typing
import
Dict
    
from
typing
import
Iterator
    
from
typing
import
Any
    
from
typing
import
Tuple
    
from
typing
import
Optional
    
from
typing
import
TypeVar
    
from
typing
import
Protocol
    
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
    
WsgiResponseIter
=
TypeVar
(
"
WsgiResponseIter
"
)
    
WsgiResponseHeaders
=
TypeVar
(
"
WsgiResponseHeaders
"
)
    
WsgiExcInfo
=
TypeVar
(
"
WsgiExcInfo
"
)
    
class
StartResponse
(
Protocol
)
:
        
def
__call__
(
self
status
response_headers
exc_info
=
None
)
:
            
pass
_wsgi_middleware_applied
=
ContextVar
(
"
sentry_wsgi_middleware_applied
"
)
if
PY2
:
    
def
wsgi_decoding_dance
(
s
charset
=
"
utf
-
8
"
errors
=
"
replace
"
)
:
        
return
s
.
decode
(
charset
errors
)
else
:
    
def
wsgi_decoding_dance
(
s
charset
=
"
utf
-
8
"
errors
=
"
replace
"
)
:
        
return
s
.
encode
(
"
latin1
"
)
.
decode
(
charset
errors
)
def
get_host
(
environ
)
:
    
"
"
"
Return
the
host
for
the
given
WSGI
environment
.
Yanked
from
Werkzeug
.
"
"
"
    
if
environ
.
get
(
"
HTTP_HOST
"
)
:
        
rv
=
environ
[
"
HTTP_HOST
"
]
        
if
environ
[
"
wsgi
.
url_scheme
"
]
=
=
"
http
"
and
rv
.
endswith
(
"
:
80
"
)
:
            
rv
=
rv
[
:
-
3
]
        
elif
environ
[
"
wsgi
.
url_scheme
"
]
=
=
"
https
"
and
rv
.
endswith
(
"
:
443
"
)
:
            
rv
=
rv
[
:
-
4
]
    
elif
environ
.
get
(
"
SERVER_NAME
"
)
:
        
rv
=
environ
[
"
SERVER_NAME
"
]
        
if
(
environ
[
"
wsgi
.
url_scheme
"
]
environ
[
"
SERVER_PORT
"
]
)
not
in
(
            
(
"
https
"
"
443
"
)
            
(
"
http
"
"
80
"
)
        
)
:
            
rv
+
=
"
:
"
+
environ
[
"
SERVER_PORT
"
]
    
else
:
        
rv
=
"
unknown
"
    
return
rv
def
get_request_url
(
environ
)
:
    
"
"
"
Return
the
absolute
URL
without
query
string
for
the
given
WSGI
    
environment
.
"
"
"
    
return
"
%
s
:
/
/
%
s
/
%
s
"
%
(
        
environ
.
get
(
"
wsgi
.
url_scheme
"
)
        
get_host
(
environ
)
        
wsgi_decoding_dance
(
environ
.
get
(
"
PATH_INFO
"
)
or
"
"
)
.
lstrip
(
"
/
"
)
    
)
class
SentryWsgiMiddleware
(
object
)
:
    
__slots__
=
(
"
app
"
)
    
def
__init__
(
self
app
)
:
        
self
.
app
=
app
    
def
__call__
(
self
environ
start_response
)
:
        
if
_wsgi_middleware_applied
.
get
(
False
)
:
            
return
self
.
app
(
environ
start_response
)
        
_wsgi_middleware_applied
.
set
(
True
)
        
try
:
            
hub
=
Hub
(
Hub
.
current
)
            
with
auto_session_tracking
(
hub
)
:
                
with
hub
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
                            
scope
.
clear_breadcrumbs
(
)
                            
scope
.
_name
=
"
wsgi
"
                            
scope
.
add_event_processor
(
                                
_make_wsgi_event_processor
(
environ
)
                            
)
                    
span
=
Span
.
continue_from_environ
(
environ
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
WSGI
request
"
                    
with
hub
.
start_span
(
span
)
as
span
:
                        
try
:
                            
rv
=
self
.
app
(
                                
environ
                                
functools
.
partial
(
                                    
_sentry_start_response
start_response
span
                                
)
                            
)
                        
except
BaseException
:
                            
reraise
(
*
_capture_exception
(
hub
)
)
        
finally
:
            
_wsgi_middleware_applied
.
set
(
False
)
        
return
_ScopedResponse
(
hub
rv
)
def
_sentry_start_response
(
    
old_start_response
    
span
    
status
    
response_headers
    
exc_info
=
None
)
:
    
with
capture_internal_exceptions
(
)
:
        
status_int
=
int
(
status
.
split
(
"
"
1
)
[
0
]
)
        
span
.
set_http_status
(
status_int
)
    
if
exc_info
is
None
:
        
return
old_start_response
(
status
response_headers
)
    
else
:
        
return
old_start_response
(
status
response_headers
exc_info
)
def
_get_environ
(
environ
)
:
    
"
"
"
    
Returns
our
whitelisted
environment
variables
.
    
"
"
"
    
keys
=
[
"
SERVER_NAME
"
"
SERVER_PORT
"
]
    
if
_should_send_default_pii
(
)
:
        
keys
+
=
[
"
REMOTE_ADDR
"
]
    
for
key
in
keys
:
        
if
key
in
environ
:
            
yield
key
environ
[
key
]
def
_get_headers
(
environ
)
:
    
"
"
"
    
Returns
only
proper
HTTP
headers
.
    
"
"
"
    
for
key
value
in
iteritems
(
environ
)
:
        
key
=
str
(
key
)
        
if
key
.
startswith
(
"
HTTP_
"
)
and
key
not
in
(
            
"
HTTP_CONTENT_TYPE
"
            
"
HTTP_CONTENT_LENGTH
"
        
)
:
            
yield
key
[
5
:
]
.
replace
(
"
_
"
"
-
"
)
.
title
(
)
value
        
elif
key
in
(
"
CONTENT_TYPE
"
"
CONTENT_LENGTH
"
)
:
            
yield
key
.
replace
(
"
_
"
"
-
"
)
.
title
(
)
value
def
get_client_ip
(
environ
)
:
    
"
"
"
    
Infer
the
user
IP
address
from
various
headers
.
This
cannot
be
used
in
    
security
sensitive
situations
since
the
value
may
be
forged
from
a
client
    
but
it
'
s
good
enough
for
the
event
payload
.
    
"
"
"
    
try
:
        
return
environ
[
"
HTTP_X_FORWARDED_FOR
"
]
.
split
(
"
"
)
[
0
]
.
strip
(
)
    
except
(
KeyError
IndexError
)
:
        
pass
    
try
:
        
return
environ
[
"
HTTP_X_REAL_IP
"
]
    
except
KeyError
:
        
pass
    
return
environ
.
get
(
"
REMOTE_ADDR
"
)
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
    
if
hub
.
client
is
not
None
:
        
e
=
exc_info
[
1
]
        
should_skip_capture
=
isinstance
(
e
SystemExit
)
and
e
.
code
in
(
0
None
)
        
if
not
should_skip_capture
:
            
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
wsgi
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
class
_ScopedResponse
(
object
)
:
    
__slots__
=
(
"
_response
"
"
_hub
"
)
    
def
__init__
(
self
hub
response
)
:
        
self
.
_hub
=
hub
        
self
.
_response
=
response
    
def
__iter__
(
self
)
:
        
iterator
=
iter
(
self
.
_response
)
        
while
True
:
            
with
self
.
_hub
:
                
try
:
                    
chunk
=
next
(
iterator
)
                
except
StopIteration
:
                    
break
                
except
BaseException
:
                    
reraise
(
*
_capture_exception
(
self
.
_hub
)
)
            
yield
chunk
    
def
close
(
self
)
:
        
with
self
.
_hub
:
            
try
:
                
self
.
_response
.
close
(
)
            
except
AttributeError
:
                
pass
            
except
BaseException
:
                
reraise
(
*
_capture_exception
(
self
.
_hub
)
)
def
_make_wsgi_event_processor
(
environ
)
:
    
client_ip
=
get_client_ip
(
environ
)
    
request_url
=
get_request_url
(
environ
)
    
query_string
=
environ
.
get
(
"
QUERY_STRING
"
)
    
method
=
environ
.
get
(
"
REQUEST_METHOD
"
)
    
env
=
dict
(
_get_environ
(
environ
)
)
    
headers
=
_filter_headers
(
dict
(
_get_headers
(
environ
)
)
)
    
def
event_processor
(
event
hint
)
:
        
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
            
if
_should_send_default_pii
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
                
if
client_ip
:
                    
user_info
.
setdefault
(
"
ip_address
"
client_ip
)
            
request_info
[
"
url
"
]
=
request_url
            
request_info
[
"
query_string
"
]
=
query_string
            
request_info
[
"
method
"
]
=
method
            
request_info
[
"
env
"
]
=
env
            
request_info
[
"
headers
"
]
=
headers
        
return
event
    
return
event_processor
