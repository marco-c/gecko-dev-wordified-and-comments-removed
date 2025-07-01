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
AuthCredentials
from
tests
.
support
.
sync
import
AsyncPoll
from
.
.
import
AUTH_REQUIRED_EVENT
RESPONSE_COMPLETED_EVENT
pytestmark
=
pytest
.
mark
.
asyncio
pytest
.
mark
.
parametrize
(
"
navigate
"
[
False
True
]
ids
=
[
"
fetch
"
"
navigate
"
]
)
async
def
test_wrong_credentials
(
    
setup_blocked_request
subscribe_events
wait_for_event
bidi_session
navigate
wait_for_future_safe
)
:
    
username
=
f
"
test_missing_credentials_
{
navigate
}
"
    
password
=
f
"
test_missing_credentials_password_
{
navigate
}
"
    
request
=
await
setup_blocked_request
(
        
"
authRequired
"
username
=
username
password
=
password
navigate
=
navigate
    
)
    
await
subscribe_events
(
events
=
[
AUTH_REQUIRED_EVENT
]
)
    
on_auth_required
=
wait_for_event
(
AUTH_REQUIRED_EVENT
)
    
wrong_credentials
=
AuthCredentials
(
username
=
username
password
=
"
wrong_password
"
)
    
await
bidi_session
.
network
.
continue_response
(
        
request
=
request
credentials
=
wrong_credentials
    
)
    
await
wait_for_future_safe
(
on_auth_required
)
pytest
.
mark
.
parametrize
(
"
navigate
"
[
False
True
]
ids
=
[
"
fetch
"
"
navigate
"
]
)
async
def
test_correct_credentials
(
    
setup_blocked_request
subscribe_events
wait_for_event
bidi_session
navigate
wait_for_future_safe
)
:
    
username
=
f
"
test_wrong_credentials_
{
navigate
}
"
    
password
=
f
"
test_wrong_credentials_password_
{
navigate
}
"
    
request
=
await
setup_blocked_request
(
        
"
authRequired
"
username
=
username
password
=
password
navigate
=
navigate
    
)
    
await
subscribe_events
(
        
events
=
[
AUTH_REQUIRED_EVENT
RESPONSE_COMPLETED_EVENT
"
browsingContext
.
load
"
]
    
)
    
response_completed_events
=
[
]
    
async
def
on_event
(
method
data
)
:
        
response_completed_events
.
append
(
data
)
    
remove_listener
=
bidi_session
.
add_event_listener
(
        
RESPONSE_COMPLETED_EVENT
on_event
    
)
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
if
navigate
:
        
on_load
=
wait_for_event
(
"
browsingContext
.
load
"
)
    
correct_credentials
=
AuthCredentials
(
username
=
username
password
=
password
)
    
await
bidi_session
.
network
.
continue_response
(
        
request
=
request
credentials
=
correct_credentials
    
)
    
await
wait_for_future_safe
(
on_response_completed
)
    
if
navigate
:
        
await
wait_for_future_safe
(
on_load
)
    
def
check_event
(
_
)
:
        
assert
len
(
            
response_completed_events
)
>
0
"
Didn
'
t
receive
response
completed
events
"
        
assert
response_completed_events
[
-
1
]
[
"
response
"
]
[
"
status
"
]
=
=
200
"
Invalid
HTTP
status
for
most
recent
event
"
    
wait
=
AsyncPoll
(
bidi_session
)
    
await
wait
.
until
(
check_event
)
    
remove_listener
(
)
