import
pytest
import
pytest_asyncio
from
tests
.
bidi
.
network
import
(
    
BEFORE_REQUEST_SENT_EVENT
    
PAGE_EMPTY_HTML
    
RESPONSE_COMPLETED_EVENT
)
from
webdriver
.
bidi
import
error
MAX_TOTAL_SIZE
=
1000
big_data
=
MAX_TOTAL_SIZE
-
100
half_size_data
=
int
(
MAX_TOTAL_SIZE
/
2
)
max_size_data
=
MAX_TOTAL_SIZE
small_data
=
int
(
MAX_TOTAL_SIZE
/
100
)
too_big_data
=
MAX_TOTAL_SIZE
+
100
too_big_one_byte_data
=
MAX_TOTAL_SIZE
+
1
pytest_asyncio
.
fixture
async
def
send_request
(
wait_for_event
inline
fetch
wait_for_future_safe
)
:
    
mode_flip
=
False
    
async
def
_send_request
(
size
mode
)
:
        
nonlocal
mode_flip
        
if
mode
=
=
"
request
or
response
"
:
            
mode_flip
=
not
mode_flip
            
data_type
=
"
request
"
if
mode_flip
else
"
response
"
        
else
:
            
data_type
=
mode
        
data
=
"
"
.
join
(
"
A
"
for
i
in
range
(
size
)
)
        
if
data_type
=
=
"
request
"
:
            
post_data
=
data
            
response_data
=
"
"
        
elif
data_type
=
=
"
response
"
:
            
response_data
=
data
            
post_data
=
None
        
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
=
inline
(
response_data
doctype
=
"
js
"
)
post_data
=
post_data
)
        
event
=
await
wait_for_future_safe
(
on_response_completed
)
        
return
{
"
request
"
:
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
"
data_type
"
:
data_type
}
    
return
_send_request
pytest
.
mark
.
capabilities
(
    
{
        
"
moz
:
firefoxOptions
"
:
{
            
"
prefs
"
:
{
                
"
remote
.
network
.
maxTotalDataSize
"
:
MAX_TOTAL_SIZE
            
}
        
}
    
}
)
pytest
.
mark
.
parametrize
(
    
"
mode
"
    
[
        
"
request
"
        
"
response
"
        
"
request
or
response
"
    
]
)
pytest
.
mark
.
asyncio
async
def
test_max_total_data_size
(
    
bidi_session
    
setup_network_test
    
top_context
    
add_data_collector
    
send_request
    
mode
)
:
    
await
setup_network_test
(
        
events
=
[
            
BEFORE_REQUEST_SENT_EVENT
            
RESPONSE_COMPLETED_EVENT
        
]
    
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
top_context
[
"
context
"
]
        
url
=
PAGE_EMPTY_HTML
        
wait
=
"
complete
"
    
)
    
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
"
response
"
]
        
max_encoded_data_size
=
MAX_TOTAL_SIZE
    
)
    
request_1_big
=
await
send_request
(
size
=
big_data
mode
=
mode
)
    
await
assert_request_data_available
(
request_1_big
bidi_session
)
    
request_2_big
=
await
send_request
(
size
=
big_data
mode
=
mode
)
    
await
assert_request_data_unavailable
(
request_1_big
bidi_session
)
    
await
assert_request_data_available
(
request_2_big
bidi_session
)
    
request_3_small
=
await
send_request
(
size
=
small_data
mode
=
mode
)
    
await
assert_request_data_available
(
request_2_big
bidi_session
)
    
await
assert_request_data_available
(
request_3_small
bidi_session
)
    
request_4_big
=
await
send_request
(
size
=
big_data
mode
=
mode
)
    
await
assert_request_data_unavailable
(
request_2_big
bidi_session
)
    
await
assert_request_data_available
(
request_3_small
bidi_session
)
    
await
assert_request_data_available
(
request_4_big
bidi_session
)
    
request_5_small
=
await
send_request
(
size
=
small_data
mode
=
mode
)
    
await
assert_request_data_available
(
request_3_small
bidi_session
)
    
await
assert_request_data_available
(
request_4_big
bidi_session
)
    
await
assert_request_data_available
(
request_5_small
bidi_session
)
    
request_6_big
=
await
send_request
(
size
=
big_data
mode
=
mode
)
    
await
assert_request_data_unavailable
(
request_3_small
bidi_session
)
    
await
assert_request_data_unavailable
(
request_4_big
bidi_session
)
    
await
assert_request_data_available
(
request_5_small
bidi_session
)
    
await
assert_request_data_available
(
request_6_big
bidi_session
)
    
request_7_too_big
=
await
send_request
(
size
=
too_big_data
mode
=
mode
)
    
await
assert_request_data_available
(
request_5_small
bidi_session
)
    
await
assert_request_data_available
(
request_6_big
bidi_session
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
request_7_too_big
[
"
request
"
]
            
data_type
=
request_7_too_big
[
"
data_type
"
]
        
)
    
request_8_too_big_one_byte
=
await
send_request
(
        
size
=
too_big_one_byte_data
mode
=
mode
    
)
    
await
assert_request_data_available
(
request_5_small
bidi_session
)
    
await
assert_request_data_available
(
request_6_big
bidi_session
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
request_8_too_big_one_byte
[
"
request
"
]
            
data_type
=
request_8_too_big_one_byte
[
"
data_type
"
]
        
)
    
request_9_max_size
=
await
send_request
(
size
=
max_size_data
mode
=
mode
)
    
await
assert_request_data_unavailable
(
request_5_small
bidi_session
)
    
await
assert_request_data_unavailable
(
request_6_big
bidi_session
)
    
await
assert_request_data_available
(
request_9_max_size
bidi_session
)
    
request_10_half_size
=
await
send_request
(
size
=
half_size_data
mode
=
mode
)
    
request_11_half_size
=
await
send_request
(
size
=
half_size_data
mode
=
mode
)
    
await
assert_request_data_unavailable
(
request_9_max_size
bidi_session
)
    
await
assert_request_data_available
(
request_10_half_size
bidi_session
)
    
await
assert_request_data_available
(
request_11_half_size
bidi_session
)
async
def
assert_request_data_available
(
request
bidi_session
)
:
    
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
[
"
request
"
]
        
data_type
=
request
[
"
data_type
"
]
    
)
    
assert
isinstance
(
data
[
"
value
"
]
str
)
async
def
assert_request_data_unavailable
(
request
bidi_session
)
:
    
with
pytest
.
raises
(
error
.
UnavailableNetworkDataException
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
[
"
request
"
]
            
data_type
=
request
[
"
data_type
"
]
        
)
