from
contextlib
import
contextmanager
import
json
from
copy
import
deepcopy
import
sentry_sdk
from
sentry_sdk
.
scope
import
should_send_default_pii
from
sentry_sdk
.
utils
import
AnnotatedValue
logger
try
:
    
from
django
.
http
.
request
import
RawPostDataException
except
ImportError
:
    
RawPostDataException
=
None
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
Iterator
    
from
typing
import
Mapping
    
from
typing
import
MutableMapping
    
from
typing
import
Optional
    
from
typing
import
Union
    
from
sentry_sdk
.
_types
import
Event
HttpStatusCodeRange
SENSITIVE_ENV_KEYS
=
(
    
"
REMOTE_ADDR
"
    
"
HTTP_X_FORWARDED_FOR
"
    
"
HTTP_SET_COOKIE
"
    
"
HTTP_COOKIE
"
    
"
HTTP_AUTHORIZATION
"
    
"
HTTP_X_API_KEY
"
    
"
HTTP_X_FORWARDED_FOR
"
    
"
HTTP_X_REAL_IP
"
)
SENSITIVE_HEADERS
=
tuple
(
    
x
[
len
(
"
HTTP_
"
)
:
]
for
x
in
SENSITIVE_ENV_KEYS
if
x
.
startswith
(
"
HTTP_
"
)
)
DEFAULT_HTTP_METHODS_TO_CAPTURE
=
(
    
"
CONNECT
"
    
"
DELETE
"
    
"
GET
"
    
"
PATCH
"
    
"
POST
"
    
"
PUT
"
    
"
TRACE
"
)
contextmanager
def
nullcontext
(
)
:
    
yield
def
request_body_within_bounds
(
client
content_length
)
:
    
if
client
is
None
:
        
return
False
    
bodies
=
client
.
options
[
"
max_request_body_size
"
]
    
return
not
(
        
bodies
=
=
"
never
"
        
or
(
bodies
=
=
"
small
"
and
content_length
>
10
*
*
3
)
        
or
(
bodies
=
=
"
medium
"
and
content_length
>
10
*
*
4
)
    
)
class
RequestExtractor
:
    
"
"
"
    
Base
class
for
request
extraction
.
    
"
"
"
    
def
__init__
(
self
request
)
:
        
self
.
request
=
request
    
def
extract_into_event
(
self
event
)
:
        
client
=
sentry_sdk
.
get_client
(
)
        
if
not
client
.
is_active
(
)
:
            
return
        
data
=
None
        
content_length
=
self
.
content_length
(
)
        
request_info
=
event
.
get
(
"
request
"
{
}
)
        
if
should_send_default_pii
(
)
:
            
request_info
[
"
cookies
"
]
=
dict
(
self
.
cookies
(
)
)
        
if
not
request_body_within_bounds
(
client
content_length
)
:
            
data
=
AnnotatedValue
.
removed_because_over_size_limit
(
)
        
else
:
            
raw_data
=
None
            
try
:
                
raw_data
=
self
.
raw_data
(
)
            
except
(
RawPostDataException
ValueError
)
:
                
pass
            
parsed_body
=
self
.
parsed_body
(
)
            
if
parsed_body
is
not
None
:
                
data
=
parsed_body
            
elif
raw_data
:
                
data
=
AnnotatedValue
.
removed_because_raw_data
(
)
            
else
:
                
data
=
None
        
if
data
is
not
None
:
            
request_info
[
"
data
"
]
=
data
        
event
[
"
request
"
]
=
deepcopy
(
request_info
)
    
def
content_length
(
self
)
:
        
try
:
            
return
int
(
self
.
env
(
)
.
get
(
"
CONTENT_LENGTH
"
0
)
)
        
except
ValueError
:
            
return
0
    
def
cookies
(
self
)
:
        
raise
NotImplementedError
(
)
    
def
raw_data
(
self
)
:
        
raise
NotImplementedError
(
)
    
def
form
(
self
)
:
        
raise
NotImplementedError
(
)
    
def
parsed_body
(
self
)
:
        
try
:
            
form
=
self
.
form
(
)
        
except
Exception
:
            
form
=
None
        
try
:
            
files
=
self
.
files
(
)
        
except
Exception
:
            
files
=
None
        
if
form
or
files
:
            
data
=
{
}
            
if
form
:
                
data
=
dict
(
form
.
items
(
)
)
            
if
files
:
                
for
key
in
files
.
keys
(
)
:
                    
data
[
key
]
=
AnnotatedValue
.
removed_because_raw_data
(
)
            
return
data
        
return
self
.
json
(
)
    
def
is_json
(
self
)
:
        
return
_is_json_content_type
(
self
.
env
(
)
.
get
(
"
CONTENT_TYPE
"
)
)
    
def
json
(
self
)
:
        
try
:
            
if
not
self
.
is_json
(
)
:
                
return
None
            
try
:
                
raw_data
=
self
.
raw_data
(
)
            
except
(
RawPostDataException
ValueError
)
:
                
raw_data
=
None
            
if
raw_data
is
None
:
                
return
None
            
if
isinstance
(
raw_data
str
)
:
                
return
json
.
loads
(
raw_data
)
            
else
:
                
return
json
.
loads
(
raw_data
.
decode
(
"
utf
-
8
"
)
)
        
except
ValueError
:
            
pass
        
return
None
    
def
files
(
self
)
:
        
raise
NotImplementedError
(
)
    
def
size_of_file
(
self
file
)
:
        
raise
NotImplementedError
(
)
    
def
env
(
self
)
:
        
raise
NotImplementedError
(
)
def
_is_json_content_type
(
ct
)
:
    
mt
=
(
ct
or
"
"
)
.
split
(
"
;
"
1
)
[
0
]
    
return
(
        
mt
=
=
"
application
/
json
"
        
or
(
mt
.
startswith
(
"
application
/
"
)
)
        
and
mt
.
endswith
(
"
+
json
"
)
    
)
def
_filter_headers
(
headers
)
:
    
if
should_send_default_pii
(
)
:
        
return
headers
    
return
{
        
k
:
(
            
v
            
if
k
.
upper
(
)
.
replace
(
"
-
"
"
_
"
)
not
in
SENSITIVE_HEADERS
            
else
AnnotatedValue
.
removed_because_over_size_limit
(
)
        
)
        
for
k
v
in
headers
.
items
(
)
    
}
def
_in_http_status_code_range
(
code
code_ranges
)
:
    
for
target
in
code_ranges
:
        
if
isinstance
(
target
int
)
:
            
if
code
=
=
target
:
                
return
True
            
continue
        
try
:
            
if
code
in
target
:
                
return
True
        
except
TypeError
:
            
logger
.
warning
(
                
"
failed_request_status_codes
has
to
be
a
list
of
integers
or
containers
"
            
)
    
return
False
class
HttpCodeRangeContainer
:
    
"
"
"
    
Wrapper
to
make
it
possible
to
use
list
[
HttpStatusCodeRange
]
as
a
Container
[
int
]
.
    
Used
for
backwards
compatibility
with
the
old
failed_request_status_codes
option
.
    
"
"
"
    
def
__init__
(
self
code_ranges
)
:
        
self
.
_code_ranges
=
code_ranges
    
def
__contains__
(
self
item
)
:
        
return
_in_http_status_code_range
(
item
self
.
_code_ranges
)
