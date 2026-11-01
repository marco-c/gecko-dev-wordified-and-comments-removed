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
pytest
.
mark
.
parametrize
(
"
disown
"
[
True
False
]
)
async
def
test_single_collector
(
bidi_session
url
setup_collected_data
disown
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
    
data
=
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
disown
    
)
    
assert
data
[
"
type
"
]
=
=
"
string
"
    
assert
data
[
"
value
"
]
=
=
"
empty
\
n
"
    
if
disown
:
        
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
    
else
:
        
data_again
=
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
        
assert
data_again
=
=
data
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
max_encoded_data_size
=
1000
    
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
    
data
=
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
    
data_from_other_collector
=
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
    
assert
data_from_other_collector
=
=
data
    
data_without_collector
=
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
    
data
=
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
collector
=
collector
disown
=
True
    
)
    
assert
data
=
=
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
test
"
}
    
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
