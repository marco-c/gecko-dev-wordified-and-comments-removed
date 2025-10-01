import
asyncio
import
random
import
uuid
import
pytest
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
    
PAGE_EMPTY_HTML
    
PAGE_EMPTY_TEXT
    
PAGE_OTHER_TEXT
    
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
test_other_url
(
    
url
    
add_intercept
    
fetch
    
setup_network_test
    
phase
)
:
    
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
fetch
(
url
(
PAGE_OTHER_TEXT
)
)
pytest
.
mark
.
asyncio
async
def
test_return_value
(
add_intercept
)
:
    
intercept
=
await
add_intercept
(
phases
=
[
"
beforeRequestSent
"
]
url_patterns
=
[
]
)
    
assert
isinstance
(
intercept
str
)
    
uuid
.
UUID
(
hex
=
intercept
)
pytest
.
mark
.
asyncio
async
def
test_two_intercepts
(
    
bidi_session
    
wait_for_event
    
url
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_future_safe
)
:
    
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
    
string_intercept
=
await
add_intercept
(
        
phases
=
[
"
beforeRequestSent
"
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
    
global_intercept
=
await
add_intercept
(
        
phases
=
[
"
beforeRequestSent
"
]
        
url_patterns
=
[
]
    
)
    
on_network_event
=
wait_for_event
(
BEFORE_REQUEST_SENT_EVENT
)
    
asyncio
.
ensure_future
(
fetch
(
text_url
)
)
    
event
=
await
wait_for_future_safe
(
on_network_event
)
    
assert_before_request_sent_event
(
        
event
is_blocked
=
True
intercepts
=
[
string_intercept
global_intercept
]
    
)
    
other_url
=
f
"
{
url
(
PAGE_OTHER_TEXT
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
    
on_network_event
=
wait_for_event
(
BEFORE_REQUEST_SENT_EVENT
)
    
asyncio
.
ensure_future
(
fetch
(
other_url
)
)
    
event
=
await
wait_for_future_safe
(
on_network_event
)
    
assert_before_request_sent_event
(
        
event
is_blocked
=
True
intercepts
=
[
global_intercept
]
    
)
    
await
bidi_session
.
network
.
remove_intercept
(
intercept
=
global_intercept
)
    
await
fetch
(
other_url
)
    
on_network_event
=
wait_for_event
(
BEFORE_REQUEST_SENT_EVENT
)
    
asyncio
.
ensure_future
(
fetch
(
text_url
)
)
    
event
=
await
wait_for_future_safe
(
on_network_event
)
    
assert_before_request_sent_event
(
        
event
is_blocked
=
True
intercepts
=
[
string_intercept
]
    
)
    
await
bidi_session
.
network
.
remove_intercept
(
intercept
=
string_intercept
)
    
await
fetch
(
text_url
)
