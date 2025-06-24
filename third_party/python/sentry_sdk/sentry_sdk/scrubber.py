try
:
    
from
typing
import
cast
except
ImportError
:
    
cast
=
lambda
_
obj
:
obj
from
sentry_sdk
.
utils
import
(
    
capture_internal_exceptions
    
AnnotatedValue
    
iter_event_frames
)
from
sentry_sdk
.
_compat
import
string_types
from
sentry_sdk
.
_types
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
sentry_sdk
.
_types
import
Event
    
from
typing
import
List
    
from
typing
import
Optional
DEFAULT_DENYLIST
=
[
    
"
password
"
    
"
passwd
"
    
"
secret
"
    
"
api_key
"
    
"
apikey
"
    
"
auth
"
    
"
credentials
"
    
"
mysql_pwd
"
    
"
privatekey
"
    
"
private_key
"
    
"
token
"
    
"
ip_address
"
    
"
session
"
    
"
csrftoken
"
    
"
sessionid
"
    
"
remote_addr
"
    
"
x_csrftoken
"
    
"
x_forwarded_for
"
    
"
set_cookie
"
    
"
cookie
"
    
"
authorization
"
    
"
x_api_key
"
    
"
x_forwarded_for
"
    
"
x_real_ip
"
    
"
aiohttp_session
"
    
"
connect
.
sid
"
    
"
csrf_token
"
    
"
csrf
"
    
"
_csrf
"
    
"
_csrf_token
"
    
"
PHPSESSID
"
    
"
_session
"
    
"
symfony
"
    
"
user_session
"
    
"
_xsrf
"
    
"
XSRF
-
TOKEN
"
]
class
EventScrubber
(
object
)
:
    
def
__init__
(
self
denylist
=
None
recursive
=
False
)
:
        
self
.
denylist
=
DEFAULT_DENYLIST
if
denylist
is
None
else
denylist
        
self
.
denylist
=
[
x
.
lower
(
)
for
x
in
self
.
denylist
]
        
self
.
recursive
=
recursive
    
def
scrub_list
(
self
lst
)
:
        
"
"
"
        
If
a
list
is
passed
to
this
method
the
method
recursively
searches
the
list
and
any
        
nested
lists
for
any
dictionaries
.
The
method
calls
scrub_dict
on
all
dictionaries
        
it
finds
.
        
If
the
parameter
passed
to
this
method
is
not
a
list
the
method
does
nothing
.
        
"
"
"
        
if
not
isinstance
(
lst
list
)
:
            
return
        
for
v
in
lst
:
            
self
.
scrub_dict
(
v
)
            
self
.
scrub_list
(
v
)
    
def
scrub_dict
(
self
d
)
:
        
"
"
"
        
If
a
dictionary
is
passed
to
this
method
the
method
scrubs
the
dictionary
of
any
        
sensitive
data
.
The
method
calls
itself
recursively
on
any
nested
dictionaries
(
        
including
dictionaries
nested
in
lists
)
if
self
.
recursive
is
True
.
        
This
method
does
nothing
if
the
parameter
passed
to
it
is
not
a
dictionary
.
        
"
"
"
        
if
not
isinstance
(
d
dict
)
:
            
return
        
for
k
v
in
d
.
items
(
)
:
            
if
isinstance
(
k
string_types
)
and
cast
(
str
k
)
.
lower
(
)
in
self
.
denylist
:
                
d
[
k
]
=
AnnotatedValue
.
substituted_because_contains_sensitive_data
(
)
            
elif
self
.
recursive
:
                
self
.
scrub_dict
(
v
)
                
self
.
scrub_list
(
v
)
    
def
scrub_request
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
if
"
request
"
in
event
:
                
if
"
headers
"
in
event
[
"
request
"
]
:
                    
self
.
scrub_dict
(
event
[
"
request
"
]
[
"
headers
"
]
)
                
if
"
cookies
"
in
event
[
"
request
"
]
:
                    
self
.
scrub_dict
(
event
[
"
request
"
]
[
"
cookies
"
]
)
                
if
"
data
"
in
event
[
"
request
"
]
:
                    
self
.
scrub_dict
(
event
[
"
request
"
]
[
"
data
"
]
)
    
def
scrub_extra
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
if
"
extra
"
in
event
:
                
self
.
scrub_dict
(
event
[
"
extra
"
]
)
    
def
scrub_user
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
if
"
user
"
in
event
:
                
self
.
scrub_dict
(
event
[
"
user
"
]
)
    
def
scrub_breadcrumbs
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
if
"
breadcrumbs
"
in
event
:
                
if
"
values
"
in
event
[
"
breadcrumbs
"
]
:
                    
for
value
in
event
[
"
breadcrumbs
"
]
[
"
values
"
]
:
                        
if
"
data
"
in
value
:
                            
self
.
scrub_dict
(
value
[
"
data
"
]
)
    
def
scrub_frames
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
for
frame
in
iter_event_frames
(
event
)
:
                
if
"
vars
"
in
frame
:
                    
self
.
scrub_dict
(
frame
[
"
vars
"
]
)
    
def
scrub_spans
(
self
event
)
:
        
with
capture_internal_exceptions
(
)
:
            
if
"
spans
"
in
event
:
                
for
span
in
event
[
"
spans
"
]
:
                    
if
"
data
"
in
span
:
                        
self
.
scrub_dict
(
span
[
"
data
"
]
)
    
def
scrub_event
(
self
event
)
:
        
self
.
scrub_request
(
event
)
        
self
.
scrub_extra
(
event
)
        
self
.
scrub_user
(
event
)
        
self
.
scrub_breadcrumbs
(
event
)
        
self
.
scrub_frames
(
event
)
        
self
.
scrub_spans
(
event
)
