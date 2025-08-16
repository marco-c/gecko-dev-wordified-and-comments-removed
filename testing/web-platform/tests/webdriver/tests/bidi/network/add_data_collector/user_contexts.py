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
.
.
import
PAGE_EMPTY_TEXT
RESPONSE_COMPLETED_EVENT
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_user_context
(
    
bidi_session
    
add_data_collector
    
create_user_context
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
    
url
    
fetch
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context_1
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
    
)
    
await
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_user_context_1
[
"
context
"
]
    
)
    
collector
=
await
add_data_collector
(
user_contexts
=
[
user_context
]
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_user_context_1
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
)
    
context_in_user_context_2
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
    
)
    
await
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_user_context_2
[
"
context
"
]
    
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_user_context_2
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
)
    
context_in_default_context
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
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_default_context
[
"
context
"
]
    
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_default_context
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
with
pytest
.
raises
(
error
.
NoSuchNetworkDataException
)
:
        
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
)
async
def
test_multiple_user_context
(
    
bidi_session
    
add_data_collector
    
create_user_context
    
setup_network_test
    
wait_for_event
    
wait_for_future_safe
    
url
    
fetch
)
:
    
user_context_a
=
await
create_user_context
(
)
    
context_in_user_context_a
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context_a
type_hint
=
"
tab
"
    
)
    
await
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_user_context_a
[
"
context
"
]
    
)
    
user_context_b
=
await
create_user_context
(
)
    
context_in_user_context_b
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context_b
type_hint
=
"
tab
"
    
)
    
await
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_user_context_b
[
"
context
"
]
    
)
    
collector
=
await
add_data_collector
(
user_contexts
=
[
user_context_a
user_context_b
]
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_user_context_a
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_user_context_b
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
)
    
context_in_default_context
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
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
context
=
context_in_default_context
[
"
context
"
]
    
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
url
(
PAGE_EMPTY_TEXT
)
context
=
context_in_default_context
)
    
event
=
await
wait_for_future_safe
(
on_response_completed
)
    
request
=
event
[
"
request
"
]
[
"
request
"
]
    
with
pytest
.
raises
(
error
.
NoSuchNetworkDataException
)
:
        
await
bidi_session
.
network
.
get_data
(
request
=
request
data_type
=
"
response
"
)
