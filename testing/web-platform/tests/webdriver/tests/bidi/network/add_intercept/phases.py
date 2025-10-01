import
pytest
import
random
from
webdriver
.
bidi
.
modules
.
script
import
ScriptEvaluateResultException
from
.
.
import
(
    
assert_before_request_sent_event
    
assert_response_event
    
PAGE_EMPTY_TEXT
    
BEFORE_REQUEST_SENT_EVENT
    
RESPONSE_COMPLETED_EVENT
    
RESPONSE_STARTED_EVENT
)
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
phases
intercepted_phase
"
    
[
        
(
[
"
beforeRequestSent
"
]
"
beforeRequestSent
"
)
        
(
[
"
responseStarted
"
]
"
responseStarted
"
)
        
(
[
"
beforeRequestSent
"
"
responseStarted
"
]
"
beforeRequestSent
"
)
        
(
[
"
responseStarted
"
"
beforeRequestSent
"
]
"
beforeRequestSent
"
)
        
(
[
"
beforeRequestSent
"
"
beforeRequestSent
"
]
"
beforeRequestSent
"
)
    
]
)
async
def
test_request_response_phases
(
    
wait_for_event
    
url
    
setup_network_test
    
add_intercept
    
fetch
    
wait_for_future_safe
    
phases
    
intercepted_phase
)
:
    
network_events
=
await
setup_network_test
(
        
events
=
[
            
BEFORE_REQUEST_SENT_EVENT
            
RESPONSE_STARTED_EVENT
            
RESPONSE_COMPLETED_EVENT
        
]
    
)
    
before_request_sent_events
=
network_events
[
BEFORE_REQUEST_SENT_EVENT
]
    
response_started_events
=
network_events
[
RESPONSE_STARTED_EVENT
]
    
response_completed_events
=
network_events
[
RESPONSE_COMPLETED_EVENT
]
    
text_url
=
f
"
{
url
(
PAGE_EMPTY_TEXT
)
}
?
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
    
intercept
=
await
add_intercept
(
        
phases
=
phases
        
url_patterns
=
[
{
"
type
"
:
"
string
"
"
pattern
"
:
text_url
}
]
    
)
    
assert
isinstance
(
intercept
str
)
    
on_network_event
=
wait_for_event
(
f
"
network
.
{
intercepted_phase
}
"
)
    
with
pytest
.
raises
(
ScriptEvaluateResultException
)
:
        
await
fetch
(
text_url
)
    
await
wait_for_future_safe
(
on_network_event
)
    
expected_request
=
{
"
method
"
:
"
GET
"
"
url
"
:
text_url
}
    
if
intercepted_phase
=
=
"
beforeRequestSent
"
:
        
assert
len
(
before_request_sent_events
)
=
=
1
        
assert
len
(
response_started_events
)
=
=
0
        
assert_before_request_sent_event
(
            
before_request_sent_events
[
0
]
            
expected_request
=
expected_request
            
is_blocked
=
True
            
intercepts
=
[
intercept
]
        
)
    
elif
intercepted_phase
=
=
"
responseStarted
"
:
        
assert
len
(
before_request_sent_events
)
=
=
1
        
assert
len
(
response_started_events
)
=
=
1
        
assert_before_request_sent_event
(
            
before_request_sent_events
[
0
]
            
expected_request
=
expected_request
            
is_blocked
=
False
        
)
        
assert_response_event
(
            
response_started_events
[
0
]
            
expected_request
=
expected_request
            
is_blocked
=
True
            
intercepts
=
[
intercept
]
        
)
    
assert
len
(
response_completed_events
)
=
=
0
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
phase
"
[
"
beforeRequestSent
"
"
responseStarted
"
]
)
async
def
test_not_listening_to_phase_event
(
    
url
    
setup_network_test
    
add_intercept
    
fetch
    
phase
)
:
    
events
=
[
        
BEFORE_REQUEST_SENT_EVENT
        
RESPONSE_STARTED_EVENT
        
RESPONSE_COMPLETED_EVENT
    
]
    
events
.
remove
(
f
"
network
.
{
phase
}
"
)
    
await
setup_network_test
(
events
=
events
)
    
text_url
=
f
"
{
url
(
PAGE_EMPTY_TEXT
)
}
?
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
    
await
add_intercept
(
        
phases
=
[
phase
]
        
url_patterns
=
[
{
"
type
"
:
"
string
"
"
pattern
"
:
text_url
}
]
    
)
    
await
fetch
(
text_url
)
