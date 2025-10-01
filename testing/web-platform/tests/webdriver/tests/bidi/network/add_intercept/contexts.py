import
asyncio
import
random
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
    
assert_response_event
    
PAGE_EMPTY_HTML
    
PAGE_EMPTY_TEXT
    
BEFORE_REQUEST_SENT_EVENT
    
RESPONSE_COMPLETED_EVENT
    
RESPONSE_STARTED_EVENT
    
PHASE_TO_EVENT_MAP
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
domain
"
[
"
"
"
alt
"
]
ids
=
[
"
same_origin
"
"
cross_origin
"
]
)
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
test_frame_context
(
    
bidi_session
    
url
    
inline
    
new_tab
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
    
domain
    
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
new_tab
[
"
context
"
]
]
    
)
    
frame_url
=
inline
(
"
<
div
>
foo
<
/
div
>
"
)
    
test_url
=
inline
(
f
"
<
iframe
src
=
'
{
frame_url
}
'
>
<
/
iframe
>
"
domain
=
domain
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
url
=
test_url
context
=
new_tab
[
"
context
"
]
wait
=
"
complete
"
    
)
    
contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
root
=
new_tab
[
"
context
"
]
)
    
assert
len
(
contexts
[
0
]
[
"
children
"
]
)
=
=
1
    
frame
=
contexts
[
0
]
[
"
children
"
]
[
0
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
        
contexts
=
[
new_tab
[
"
context
"
]
]
    
)
    
[
event_name
assert_network_event
]
=
PHASE_TO_EVENT_MAP
[
phase
]
    
on_network_event
=
wait_for_event
(
event_name
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
frame
)
)
    
event
=
await
wait_for_future_safe
(
on_network_event
)
    
assert_network_event
(
event
is_blocked
=
True
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
    
new_tab
    
add_intercept
    
fetch
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
    
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
new_tab
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
    
text_url_other
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
othercontext
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
pattern
"
"
pathname
"
:
PAGE_EMPTY_TEXT
}
]
    
)
    
[
event_name
assert_network_event
]
=
PHASE_TO_EVENT_MAP
[
phase
]
    
on_network_event
=
wait_for_event
(
event_name
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
new_tab
)
)
    
event
=
await
wait_for_future_safe
(
on_network_event
)
    
assert_network_event
(
event
is_blocked
=
True
)
    
await
asyncio
.
ensure_future
(
fetch
(
text_url_other
context
=
other_context
)
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
    
new_tab
    
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
new_tab
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
new_tab
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
new_tab
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
    
new_tab
    
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
new_tab
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
new_tab
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
new_tab
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
    
new_tab
    
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
new_tab
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
new_tab
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
new_tab
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
