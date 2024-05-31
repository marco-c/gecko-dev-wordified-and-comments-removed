import
asyncio
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
test_other_context
(
    
bidi_session
    
url
    
top_context
    
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
        
contexts
=
[
top_context
[
"
context
"
]
]
    
)
    
other_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
other_context
[
"
context
"
]
url
=
url
(
PAGE_EMPTY_HTML
)
wait
=
"
complete
"
    
)
    
text_url
=
url
(
PAGE_EMPTY_TEXT
)
    
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
context
=
top_context
)
    
await
fetch
(
text_url
context
=
other_context
)
pytest
.
mark
.
asyncio
async
def
test_other_context_with_event_subscription
(
    
bidi_session
    
url
    
top_context
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
)
:
    
other_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
other_context
[
"
context
"
]
url
=
url
(
PAGE_EMPTY_HTML
)
wait
=
"
complete
"
    
)
    
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
        
contexts
=
[
top_context
[
"
context
"
]
other_context
[
"
context
"
]
]
    
)
    
text_url
=
url
(
PAGE_EMPTY_TEXT
)
    
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
        
contexts
=
[
top_context
[
"
context
"
]
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
context
=
top_context
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
context
=
other_context
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
False
    
)
pytest
.
mark
.
asyncio
async
def
test_two_contexts_same_intercept
(
    
bidi_session
    
url
    
top_context
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
)
:
    
other_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
other_context
[
"
context
"
]
url
=
url
(
PAGE_EMPTY_HTML
)
wait
=
"
complete
"
    
)
    
await
setup_network_test
(
        
events
=
[
            
BEFORE_REQUEST_SENT_EVENT
        
]
        
contexts
=
[
top_context
[
"
context
"
]
other_context
[
"
context
"
]
]
    
)
    
text_url
=
url
(
PAGE_EMPTY_TEXT
)
    
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
        
contexts
=
[
top_context
[
"
context
"
]
other_context
[
"
context
"
]
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
context
=
top_context
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
intercept
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
context
=
other_context
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
intercept
]
    
)
pytest
.
mark
.
asyncio
async
def
test_two_contexts_global_intercept
(
    
bidi_session
    
url
    
top_context
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
)
:
    
other_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
other_context
[
"
context
"
]
url
=
url
(
PAGE_EMPTY_HTML
)
wait
=
"
complete
"
    
)
    
await
setup_network_test
(
        
events
=
[
            
BEFORE_REQUEST_SENT_EVENT
        
]
        
contexts
=
[
top_context
[
"
context
"
]
other_context
[
"
context
"
]
]
    
)
    
text_url
=
url
(
PAGE_EMPTY_TEXT
)
    
context_intercept
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
        
contexts
=
[
top_context
[
"
context
"
]
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
context
=
top_context
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
context_intercept
global_intercept
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
context
=
other_context
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
