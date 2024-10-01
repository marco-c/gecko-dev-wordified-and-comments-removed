import
random
import
urllib
from
datetime
import
datetime
timedelta
timezone
from
webdriver
.
bidi
.
modules
.
network
import
(
    
NetworkStringValue
    
SetCookieHeader
)
from
.
.
import
(
    
any_bool
    
any_dict
    
any_int
    
any_number
    
any_int_or_null
    
any_list
    
any_string
    
any_string_or_null
    
assert_cookies
    
int_interval
    
recursive_compare
)
def
assert_bytes_value
(
bytes_value
)
:
    
assert
bytes_value
[
"
type
"
]
in
[
"
string
"
"
base64
"
]
    
any_string
(
bytes_value
[
"
value
"
]
)
def
assert_headers
(
event_headers
expected_headers
)
:
    
assert
len
(
event_headers
)
>
=
len
(
expected_headers
)
    
for
header
in
expected_headers
:
        
assert
next
(
h
for
h
in
event_headers
if
header
=
=
h
)
is
not
None
def
assert_timing_info
(
timing_info
expected_time_range
=
None
)
:
    
time_origin
=
timing_info
.
get
(
"
timeOrigin
"
)
    
any_number
(
time_origin
)
    
def
assert_timing
(
actual
)
:
        
any_number
(
actual
)
        
if
expected_time_range
is
not
None
and
actual
!
=
0
:
            
expected_time_range
(
actual
+
time_origin
)
    
recursive_compare
(
        
{
            
"
requestTime
"
:
assert_timing
            
"
redirectStart
"
:
assert_timing
            
"
redirectEnd
"
:
assert_timing
            
"
fetchStart
"
:
assert_timing
            
"
dnsStart
"
:
assert_timing
            
"
dnsEnd
"
:
assert_timing
            
"
connectStart
"
:
assert_timing
            
"
connectEnd
"
:
assert_timing
            
"
tlsStart
"
:
assert_timing
            
"
requestStart
"
:
assert_timing
            
"
responseStart
"
:
assert_timing
            
"
responseEnd
"
:
assert_timing
        
}
        
timing_info
    
)
def
assert_request_data
(
request_data
expected_request
expected_time_range
)
:
    
recursive_compare
(
        
{
            
"
bodySize
"
:
any_int_or_null
            
"
cookies
"
:
any_list
            
"
headers
"
:
any_list
            
"
headersSize
"
:
any_int
            
"
method
"
:
any_string
            
"
request
"
:
any_string
            
"
timings
"
:
any_dict
            
"
url
"
:
any_string
        
}
        
request_data
    
)
    
for
cookie
in
request_data
[
"
cookies
"
]
:
        
assert_bytes_value
(
cookie
[
"
value
"
]
)
    
if
"
cookies
"
in
expected_request
:
        
assert_cookies
(
request_data
[
"
cookies
"
]
expected_request
[
"
cookies
"
]
)
        
del
expected_request
[
"
cookies
"
]
    
for
header
in
request_data
[
"
headers
"
]
:
        
assert_bytes_value
(
header
[
"
value
"
]
)
    
if
"
headers
"
in
expected_request
:
        
assert_headers
(
request_data
[
"
headers
"
]
expected_request
[
"
headers
"
]
)
        
del
expected_request
[
"
headers
"
]
    
assert_timing_info
(
request_data
[
"
timings
"
]
expected_time_range
)
    
recursive_compare
(
expected_request
request_data
)
def
assert_base_parameters
(
    
event
    
context
=
None
    
intercepts
=
None
    
is_blocked
=
None
    
navigation
=
None
    
redirect_count
=
None
    
expected_request
=
None
    
expected_time_range
=
None
)
:
    
recursive_compare
(
        
{
            
"
context
"
:
any_string_or_null
            
"
isBlocked
"
:
any_bool
            
"
navigation
"
:
any_string_or_null
            
"
redirectCount
"
:
any_int
            
"
request
"
:
any_dict
            
"
timestamp
"
:
any_int
        
}
        
event
    
)
    
if
context
is
not
None
:
        
assert
event
[
"
context
"
]
=
=
context
    
if
is_blocked
is
not
None
:
        
assert
event
[
"
isBlocked
"
]
=
=
is_blocked
    
if
event
[
"
isBlocked
"
]
:
        
assert
isinstance
(
event
[
"
intercepts
"
]
list
)
        
assert
len
(
event
[
"
intercepts
"
]
)
>
0
        
for
intercept
in
event
[
"
intercepts
"
]
:
            
assert
isinstance
(
intercept
str
)
    
else
:
        
assert
"
intercepts
"
not
in
event
    
if
intercepts
is
not
None
:
        
assert
event
[
"
intercepts
"
]
=
=
intercepts
    
if
navigation
is
not
None
:
        
assert
event
[
"
navigation
"
]
=
=
navigation
    
if
redirect_count
is
not
None
:
        
assert
event
[
"
redirectCount
"
]
=
=
redirect_count
    
if
expected_request
is
not
None
:
        
assert_request_data
(
event
[
"
request
"
]
expected_request
expected_time_range
)
def
assert_before_request_sent_event
(
    
event
    
context
=
None
    
intercepts
=
None
    
is_blocked
=
None
    
navigation
=
None
    
redirect_count
=
None
    
expected_request
=
None
    
expected_time_range
=
None
)
:
    
assert
isinstance
(
event
[
"
initiator
"
]
dict
)
    
assert
isinstance
(
event
[
"
initiator
"
]
[
"
type
"
]
str
)
    
assert_base_parameters
(
        
event
        
context
=
context
        
intercepts
=
intercepts
        
is_blocked
=
is_blocked
        
navigation
=
navigation
        
redirect_count
=
redirect_count
        
expected_request
=
expected_request
        
expected_time_range
=
expected_time_range
    
)
def
assert_fetch_error_event
(
    
event
    
context
=
None
    
errorText
=
None
    
intercepts
=
None
    
is_blocked
=
None
    
navigation
=
None
    
redirect_count
=
None
    
expected_request
=
None
    
expected_time_range
=
None
)
:
    
assert
isinstance
(
event
[
"
errorText
"
]
str
)
    
if
errorText
is
not
None
:
        
assert
event
[
"
errorText
"
]
=
=
errorText
    
assert_base_parameters
(
        
event
        
context
=
context
        
intercepts
=
intercepts
        
is_blocked
=
is_blocked
        
navigation
=
navigation
        
redirect_count
=
redirect_count
        
expected_request
=
expected_request
        
expected_time_range
=
expected_time_range
    
)
def
assert_response_data
(
response_data
expected_response
)
:
    
recursive_compare
(
        
{
            
"
bodySize
"
:
any_int_or_null
            
"
bytesReceived
"
:
any_int
            
"
content
"
:
{
                
"
size
"
:
any_int_or_null
            
}
            
"
fromCache
"
:
any_bool
            
"
headersSize
"
:
any_int_or_null
            
"
protocol
"
:
any_string
            
"
status
"
:
any_int
            
"
statusText
"
:
any_string
            
"
url
"
:
any_string
        
}
        
response_data
    
)
    
for
header
in
response_data
[
"
headers
"
]
:
        
assert_bytes_value
(
header
[
"
value
"
]
)
    
for
header
in
response_data
[
"
headers
"
]
:
        
assert_bytes_value
(
header
[
"
value
"
]
)
    
if
"
headers
"
in
expected_response
:
        
assert_headers
(
response_data
[
"
headers
"
]
expected_response
[
"
headers
"
]
)
        
del
expected_response
[
"
headers
"
]
    
if
response_data
[
"
status
"
]
in
[
401
407
]
:
        
assert
isinstance
(
response_data
[
"
authChallenges
"
]
list
)
    
else
:
        
assert
"
authChallenges
"
not
in
response_data
    
recursive_compare
(
expected_response
response_data
)
def
assert_response_event
(
    
event
    
context
=
None
    
intercepts
=
None
    
is_blocked
=
None
    
navigation
=
None
    
redirect_count
=
None
    
expected_request
=
None
    
expected_response
=
None
    
expected_time_range
=
None
)
:
    
any_dict
(
event
[
"
response
"
]
)
    
if
expected_response
is
not
None
:
        
assert_response_data
(
event
[
"
response
"
]
expected_response
)
    
assert_base_parameters
(
        
event
        
context
=
context
        
intercepts
=
intercepts
        
is_blocked
=
is_blocked
        
navigation
=
navigation
        
redirect_count
=
redirect_count
        
expected_request
=
expected_request
        
expected_time_range
=
expected_time_range
    
)
def
create_cookie_header
(
overrides
=
None
value_overrides
=
None
)
:
    
return
create_header
(
overrides
value_overrides
)
def
create_header
(
overrides
=
None
value_overrides
=
None
)
:
    
header
=
{
        
"
name
"
:
"
test
"
        
"
value
"
:
{
            
"
type
"
:
"
string
"
            
"
value
"
:
"
foo
"
        
}
    
}
    
if
overrides
is
not
None
:
        
header
.
update
(
overrides
)
    
if
value_overrides
is
not
None
:
        
header
[
"
value
"
]
.
update
(
value_overrides
)
    
return
header
def
get_cached_url
(
content_type
response
)
:
    
"
"
"
    
Build
a
URL
for
a
resource
which
will
be
fully
cached
.
    
:
param
content_type
:
Response
content
type
eg
"
text
/
css
"
.
    
:
param
response
:
Response
body
>
    
:
return
:
Relative
URL
as
a
string
typically
should
be
used
with
the
        
url
fixture
.
    
"
"
"
    
query_string
=
f
"
status
=
200
&
contenttype
=
{
content_type
}
&
response
=
{
response
}
&
nocache
=
{
random
.
random
(
)
}
"
    
return
f
"
/
webdriver
/
tests
/
support
/
http_handlers
/
cached
.
py
?
{
query_string
}
"
HTTP_STATUS_AND_STATUS_TEXT
=
[
    
(
101
"
Switching
Protocols
"
)
    
(
200
"
OK
"
)
    
(
201
"
Created
"
)
    
(
202
"
Accepted
"
)
    
(
203
"
Non
-
Authoritative
Information
"
)
    
(
204
"
No
Content
"
)
    
(
205
"
Reset
Content
"
)
    
(
206
"
Partial
Content
"
)
    
(
300
"
Multiple
Choices
"
)
    
(
301
"
Moved
Permanently
"
)
    
(
302
"
Found
"
)
    
(
303
"
See
Other
"
)
    
(
305
"
Use
Proxy
"
)
    
(
307
"
Temporary
Redirect
"
)
    
(
400
"
Bad
Request
"
)
    
(
401
"
Unauthorized
"
)
    
(
402
"
Payment
Required
"
)
    
(
403
"
Forbidden
"
)
    
(
404
"
Not
Found
"
)
    
(
405
"
Method
Not
Allowed
"
)
    
(
406
"
Not
Acceptable
"
)
    
(
407
"
Proxy
Authentication
Required
"
)
    
(
408
"
Request
Timeout
"
)
    
(
409
"
Conflict
"
)
    
(
410
"
Gone
"
)
    
(
411
"
Length
Required
"
)
    
(
412
"
Precondition
Failed
"
)
    
(
415
"
Unsupported
Media
Type
"
)
    
(
417
"
Expectation
Failed
"
)
    
(
500
"
Internal
Server
Error
"
)
    
(
501
"
Not
Implemented
"
)
    
(
502
"
Bad
Gateway
"
)
    
(
503
"
Service
Unavailable
"
)
    
(
504
"
Gateway
Timeout
"
)
    
(
505
"
HTTP
Version
Not
Supported
"
)
]
PAGE_DATA_URL_HTML
=
"
data
:
text
/
html
<
div
>
foo
<
/
div
>
"
PAGE_DATA_URL_IMAGE
=
"
data
:
image
/
png
;
base64
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEX
/
TQBcNTh
/
AAAAAXRSTlPM0jRW
/
QAAAApJREFUeJxjYgAAAAYAAzY3fKgAAAAASUVORK5CYII
=
"
PAGE_EMPTY_HTML
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
empty
.
html
"
PAGE_EMPTY_IMAGE
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
empty
.
png
"
PAGE_EMPTY_SCRIPT
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
empty
.
js
"
PAGE_EMPTY_SVG
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
empty
.
svg
"
PAGE_EMPTY_TEXT
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
empty
.
txt
"
PAGE_INVALID_URL
=
"
https
:
/
/
not_a_valid_url
.
test
/
"
PAGE_OTHER_TEXT
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
other
.
txt
"
PAGE_PROVIDE_RESPONSE_HTML
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
provide_response
.
html
"
PAGE_PROVIDE_RESPONSE_SCRIPT
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
provide_response
.
js
"
PAGE_PROVIDE_RESPONSE_STYLESHEET
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
provide_response
.
css
"
PAGE_REDIRECT_HTTP_EQUIV
=
(
    
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
redirect_http_equiv
.
html
"
)
PAGE_REDIRECTED_HTML
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
redirected
.
html
"
PAGE_SERVICEWORKER_HTML
=
"
/
webdriver
/
tests
/
bidi
/
network
/
support
/
serviceworker
.
html
"
STYLESHEET_GREY_BACKGROUND
=
urllib
.
parse
.
quote_plus
(
"
html
body
{
background
-
color
:
#
ccc
;
}
"
)
STYLESHEET_RED_COLOR
=
urllib
.
parse
.
quote_plus
(
"
html
body
{
color
:
red
;
}
"
)
AUTH_REQUIRED_EVENT
=
"
network
.
authRequired
"
BEFORE_REQUEST_SENT_EVENT
=
"
network
.
beforeRequestSent
"
FETCH_ERROR_EVENT
=
"
network
.
fetchError
"
RESPONSE_COMPLETED_EVENT
=
"
network
.
responseCompleted
"
RESPONSE_STARTED_EVENT
=
"
network
.
responseStarted
"
PHASE_TO_EVENT_MAP
=
{
    
"
authRequired
"
:
[
AUTH_REQUIRED_EVENT
assert_response_event
]
    
"
beforeRequestSent
"
:
[
BEFORE_REQUEST_SENT_EVENT
assert_before_request_sent_event
]
    
"
responseStarted
"
:
[
RESPONSE_STARTED_EVENT
assert_response_event
]
}
expires_a_day_from_now
=
datetime
.
now
(
timezone
.
utc
)
+
timedelta
(
days
=
1
)
expires_a_day_from_now_timestamp
=
int
(
expires_a_day_from_now
.
timestamp
(
)
)
expires_interval
=
int_interval
(
    
expires_a_day_from_now_timestamp
-
1
    
expires_a_day_from_now_timestamp
+
1
)
SET_COOKIE_TEST_PARAMETERS
=
[
    
(
        
SetCookieHeader
(
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
"
default
domain
"
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
"
alt
domain
"
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
name
=
"
foo
"
            
path
=
"
/
some
/
other
/
path
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
some
/
other
/
path
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
http_only
=
True
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
True
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
name
=
"
foo
"
            
path
=
"
/
"
            
secure
=
True
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
True
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
expiry
=
expires_a_day_from_now
.
strftime
(
"
%
a
%
d
%
b
%
Y
%
H
:
%
M
:
%
S
"
)
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
expiry
"
:
expires_interval
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
max_age
=
3600
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
expiry
"
:
any_int
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
same_site
=
"
none
"
            
secure
=
True
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
none
"
            
"
secure
"
:
True
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
same_site
=
"
lax
"
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
lax
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
    
(
        
SetCookieHeader
(
            
same_site
=
"
strict
"
            
name
=
"
foo
"
            
path
=
"
/
"
            
value
=
NetworkStringValue
(
"
bar
"
)
        
)
        
None
        
{
            
"
httpOnly
"
:
False
            
"
name
"
:
"
foo
"
            
"
path
"
:
"
/
"
            
"
sameSite
"
:
"
strict
"
            
"
secure
"
:
False
            
"
size
"
:
6
            
"
value
"
:
{
"
type
"
:
"
string
"
"
value
"
:
"
bar
"
}
        
}
    
)
]
SET_COOKIE_TEST_IDS
=
[
    
"
no
domain
"
    
"
default
domain
"
    
"
alt
domain
"
    
"
custom
path
"
    
"
http
only
"
    
"
secure
"
    
"
expiry
"
    
"
max
age
"
    
"
same
site
none
"
    
"
same
site
lax
"
    
"
same
site
strict
"
]
