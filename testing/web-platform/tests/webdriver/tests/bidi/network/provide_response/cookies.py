import
pytest
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
    
CookieHeader
    
Header
    
NetworkStringValue
    
SetCookieHeader
)
from
.
.
import
(
    
assert_response_event
    
PAGE_EMPTY_TEXT
    
PAGE_PROVIDE_RESPONSE_HTML
    
RESPONSE_COMPLETED_EVENT
    
RESPONSE_STARTED_EVENT
)
from
.
.
.
import
any_int
recursive_compare
pytestmark
=
pytest
.
mark
.
asyncio
LOAD_EVENT
=
"
browsingContext
.
load
"
async
def
test_cookie_before_request_sent
(
    
setup_blocked_request
    
subscribe_events
    
bidi_session
    
top_context
    
wait_for_event
    
wait_for_future_safe
    
fetch
    
url
)
:
    
request
=
await
setup_blocked_request
(
        
phase
=
"
beforeRequestSent
"
        
navigate
=
True
        
blocked_url
=
url
(
PAGE_PROVIDE_RESPONSE_HTML
)
        
navigate_url
=
url
(
PAGE_PROVIDE_RESPONSE_HTML
)
    
)
    
await
subscribe_events
(
        
events
=
[
            
RESPONSE_COMPLETED_EVENT
            
RESPONSE_STARTED_EVENT
            
LOAD_EVENT
        
]
    
)
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
on_load
=
wait_for_event
(
LOAD_EVENT
)
    
cookie_name
=
"
test
-
cookie
"
    
cookie_value
=
"
test
-
cookie
-
value
"
    
request_cookie
=
CookieHeader
(
        
name
=
cookie_name
value
=
NetworkStringValue
(
cookie_value
)
    
)
    
response_cookie
=
SetCookieHeader
(
        
name
=
cookie_name
value
=
NetworkStringValue
(
cookie_value
)
path
=
"
/
"
    
)
    
set_cookie_header
=
Header
(
        
name
=
"
Set
-
Cookie
"
        
value
=
NetworkStringValue
(
"
test
-
cookie
=
test
-
cookie
-
value
;
Path
=
/
"
)
    
)
    
await
bidi_session
.
network
.
provide_response
(
        
request
=
request
        
body
=
NetworkStringValue
(
"
<
div
>
Test
cookies
for
provideResponse
<
/
div
>
"
)
        
status_code
=
200
        
reason_phrase
=
"
OK
"
        
cookies
=
[
response_cookie
]
    
)
    
response_started_event
=
await
wait_for_future_safe
(
on_response_started
)
    
assert_response_event
(
        
response_started_event
expected_response
=
{
"
headers
"
:
[
set_cookie_header
]
}
    
)
    
response_completed_event
=
await
wait_for_future_safe
(
on_response_completed
)
    
assert_response_event
(
        
response_completed_event
expected_response
=
{
"
headers
"
:
[
set_cookie_header
]
}
    
)
    
await
wait_for_future_safe
(
on_load
)
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
await
fetch
(
PAGE_EMPTY_TEXT
)
    
response_completed_event
=
await
wait_for_future_safe
(
on_response_completed
)
    
assert_response_event
(
        
response_completed_event
expected_request
=
{
"
cookies
"
:
[
request_cookie
]
}
    
)
    
await
bidi_session
.
storage
.
delete_cookies
(
)
pytest
.
mark
.
parametrize
(
    
"
cookie
with_domain
expected_cookie
"
    
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
"
Tue
14
Feb
2040
17
:
41
:
14
GMT
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
expiry
"
:
2212854074
                
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
    
ids
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
)
async
def
test_cookie_attributes_before_request_sent
(
    
setup_blocked_request
    
subscribe_events
    
bidi_session
    
top_context
    
wait_for_event
    
wait_for_future_safe
    
url
    
domain_value
    
cookie
    
with_domain
    
expected_cookie
)
:
    
if
with_domain
=
=
"
default
domain
"
:
        
domain
=
"
"
        
cookie
[
"
domain
"
]
=
domain_value
(
)
        
expected_cookie
[
"
domain
"
]
=
f
"
.
{
domain_value
(
)
}
"
    
elif
with_domain
=
=
"
alt
domain
"
:
        
domain
=
"
alt
"
        
cookie
[
"
domain
"
]
=
domain_value
(
"
alt
"
)
        
expected_cookie
[
"
domain
"
]
=
f
"
.
{
domain_value
(
'
alt
'
)
}
"
    
else
:
        
domain
=
"
"
        
expected_cookie
[
"
domain
"
]
=
domain_value
(
)
    
request
=
await
setup_blocked_request
(
        
phase
=
"
beforeRequestSent
"
        
navigate
=
True
        
blocked_url
=
url
(
PAGE_PROVIDE_RESPONSE_HTML
domain
=
domain
)
    
)
    
await
subscribe_events
(
events
=
[
LOAD_EVENT
]
)
    
on_load
=
wait_for_event
(
LOAD_EVENT
)
    
await
bidi_session
.
network
.
provide_response
(
        
request
=
request
        
body
=
NetworkStringValue
(
"
<
div
>
Test
cookies
for
provideResponse
<
/
div
>
"
)
        
status_code
=
200
        
reason_phrase
=
"
OK
"
        
cookies
=
[
cookie
]
    
)
    
await
wait_for_future_safe
(
on_load
)
    
cookies
=
await
bidi_session
.
storage
.
get_cookies
(
)
    
assert
len
(
cookies
[
"
cookies
"
]
)
=
=
1
    
cookie
=
cookies
[
"
cookies
"
]
[
0
]
    
recursive_compare
(
expected_cookie
cookie
)
    
await
bidi_session
.
storage
.
delete_cookies
(
)
async
def
test_no_cookie_before_request_sent
(
    
setup_blocked_request
    
subscribe_events
    
bidi_session
    
top_context
    
wait_for_event
    
wait_for_future_safe
    
url
)
:
    
request
=
await
setup_blocked_request
(
        
phase
=
"
beforeRequestSent
"
        
navigate
=
True
        
blocked_url
=
url
(
PAGE_PROVIDE_RESPONSE_HTML
)
        
navigate_url
=
url
(
PAGE_PROVIDE_RESPONSE_HTML
)
    
)
    
await
subscribe_events
(
        
events
=
[
            
RESPONSE_COMPLETED_EVENT
            
RESPONSE_STARTED_EVENT
            
LOAD_EVENT
        
]
    
)
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
on_load
=
wait_for_event
(
LOAD_EVENT
)
    
await
bidi_session
.
network
.
provide_response
(
        
request
=
request
        
body
=
NetworkStringValue
(
"
<
div
>
Test
cookies
for
provideResponse
<
/
div
>
"
)
        
status_code
=
200
        
reason_phrase
=
"
OK
"
        
cookies
=
[
]
    
)
    
async
def
wait_for_event_and_assert_no_cookie
(
on_response_event
)
:
        
response_event
=
await
wait_for_future_safe
(
on_response_event
)
        
response_headers
=
response_event
[
"
response
"
]
[
"
headers
"
]
        
assert
len
(
[
h
for
h
in
response_headers
if
h
[
"
name
"
]
=
=
"
Set
-
Cookie
"
]
)
=
=
0
    
await
wait_for_event_and_assert_no_cookie
(
on_response_started
)
    
await
wait_for_event_and_assert_no_cookie
(
on_response_completed
)
    
await
wait_for_future_safe
(
on_load
)
    
await
bidi_session
.
storage
.
delete_cookies
(
)
