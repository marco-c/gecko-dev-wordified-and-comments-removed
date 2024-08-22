import
pytest
import
webdriver
.
bidi
.
error
as
error
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
webdriver
.
error
import
TimeoutException
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
(
    
assert_response_event
    
AUTH_REQUIRED_EVENT
    
RESPONSE_COMPLETED_EVENT
)
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_cancel
(
    
setup_blocked_request
subscribe_events
wait_for_event
bidi_session
wait_for_future_safe
)
:
    
request
=
await
setup_blocked_request
(
"
authRequired
"
)
    
await
subscribe_events
(
events
=
[
RESPONSE_COMPLETED_EVENT
]
)
    
events
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
        
events
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
    
await
bidi_session
.
network
.
continue_with_auth
(
request
=
request
action
=
"
cancel
"
)
    
response_event
=
await
wait_for_future_safe
(
on_response_completed
)
    
assert_response_event
(
        
response_event
        
expected_response
=
{
            
"
status
"
:
401
            
"
statusText
"
:
"
Unauthorized
"
        
}
    
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
1
)
    
remove_listener
(
)
async
def
test_default
(
    
setup_blocked_request
subscribe_events
bidi_session
)
:
    
request
=
await
setup_blocked_request
(
"
authRequired
"
)
    
await
subscribe_events
(
events
=
[
"
network
"
]
)
    
events
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
        
events
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
    
await
bidi_session
.
network
.
continue_with_auth
(
request
=
request
action
=
"
default
"
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
0
)
    
remove_listener
(
)
async
def
test_provideCredentials
(
    
setup_blocked_request
subscribe_events
wait_for_event
bidi_session
wait_for_future_safe
)
:
    
username
=
"
test_provideCredentials
"
    
password
=
"
test_provideCredentials_password
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
)
    
await
subscribe_events
(
events
=
[
RESPONSE_COMPLETED_EVENT
]
)
    
events
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
        
events
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
    
credentials
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
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
await
bidi_session
.
network
.
continue_with_auth
(
        
request
=
request
action
=
"
provideCredentials
"
credentials
=
credentials
    
)
    
response_event
=
await
wait_for_future_safe
(
on_response_completed
)
    
assert_response_event
(
        
response_event
        
expected_response
=
{
            
"
status
"
:
200
            
"
statusText
"
:
"
OK
"
        
}
    
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
1
)
    
remove_listener
(
)
async
def
test_provideCredentials_wrong_credentials
(
    
setup_blocked_request
subscribe_events
bidi_session
wait_for_event
wait_for_future_safe
)
:
    
username
=
"
test_provideCredentials_wrong_credentials
"
    
password
=
"
test_provideCredentials_wrong_credentials_password
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
)
    
await
subscribe_events
(
events
=
[
RESPONSE_COMPLETED_EVENT
]
)
    
events
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
        
events
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
continue_with_auth
(
        
request
=
request
action
=
"
provideCredentials
"
credentials
=
wrong_credentials
    
)
    
await
wait_for_future_safe
(
on_auth_required
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
    
on_response_completed
=
wait_for_event
(
RESPONSE_COMPLETED_EVENT
)
    
await
bidi_session
.
network
.
continue_with_auth
(
        
request
=
request
action
=
"
provideCredentials
"
credentials
=
correct_credentials
    
)
    
response_event
=
await
wait_for_future_safe
(
on_response_completed
)
    
assert_response_event
(
        
response_event
        
expected_response
=
{
            
"
status
"
:
200
            
"
statusText
"
:
"
OK
"
        
}
    
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
1
)
    
remove_listener
(
)
