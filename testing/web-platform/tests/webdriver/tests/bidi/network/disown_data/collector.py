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
    
setup_collected_response
)
:
    
[
request
collector
]
=
await
setup_collected_response
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
    
setup_collected_response
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
setup_collected_response
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
