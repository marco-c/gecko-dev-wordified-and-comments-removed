import
json
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
AnnotatedValue
from
sentry_sdk
.
_compat
import
text_type
iteritems
from
sentry_sdk
.
_types
import
MYPY
if
MYPY
:
    
import
sentry_sdk
    
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
typing
import
Union
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
request_bodies
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
(
object
)
:
    
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
Hub
.
current
.
client
        
if
client
is
None
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
_should_send_default_pii
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
self
.
raw_data
(
)
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
request_info
    
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
        
form
=
self
.
form
(
)
        
files
=
self
.
files
(
)
        
if
form
or
files
:
            
data
=
dict
(
iteritems
(
form
)
)
            
for
key
_
in
iteritems
(
files
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
            
raw_data
=
self
.
raw_data
(
)
            
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
text_type
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
_should_send_default_pii
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
iteritems
(
headers
)
    
}
