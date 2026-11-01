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
test_disowned_collector
(
    
bidi_session
    
url
    
setup_collected_data
)
:
    
[
request
collector
]
=
await
setup_collected_data
(
fetch_url
=
url
(
PAGE_EMPTY_TEXT
)
)
    
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
collector
=
collector
disown
=
True
    
)
    
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
disown_data
(
            
request
=
request
data_type
=
"
response
"
collector
=
collector
        
)
async
def
test_several_collectors
(
    
bidi_session
    
url
    
add_data_collector
    
setup_collected_data
)
:
    
collector
=
await
add_data_collector
(
collector_type
=
"
blob
"
data_types
=
[
"
response
"
]
)
    
[
request
other_collector
]
=
await
setup_collected_data
(
        
fetch_url
=
url
(
PAGE_EMPTY_TEXT
)
    
)
    
await
bidi_session
.
network
.
disown_data
(
        
request
=
request
data_type
=
"
response
"
collector
=
collector
    
)
    
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
disown_data
(
            
request
=
request
data_type
=
"
response
"
collector
=
collector
        
)
    
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
collector
=
collector
        
)
    
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
collector
=
other_collector
    
)
    
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
    
await
bidi_session
.
network
.
disown_data
(
        
request
=
request
data_type
=
"
response
"
collector
=
other_collector
    
)
    
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
disown_data
(
            
request
=
request
data_type
=
"
response
"
collector
=
other_collector
        
)
    
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
test_disown_blocked_request
(
    
bidi_session
    
add_data_collector
    
setup_blocked_request
    
subscribe_events
    
wait_for_event
    
wait_for_future_safe
)
:
    
collector
=
await
add_data_collector
(
        
collector_type
=
"
blob
"
data_types
=
[
"
request
"
]
    
)
    
request
=
await
setup_blocked_request
(
"
beforeRequestSent
"
post_data
=
"
test
"
)
    
await
bidi_session
.
network
.
disown_data
(
        
request
=
request
data_type
=
"
request
"
collector
=
collector
    
)
    
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
request
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
continue_request
(
request
=
request
)
    
await
wait_for_future_safe
(
on_response_completed
)
    
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
request
"
)
