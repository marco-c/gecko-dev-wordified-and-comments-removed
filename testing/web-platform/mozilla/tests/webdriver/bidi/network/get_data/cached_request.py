import
pytest
from
tests
.
bidi
import
wait_for_bidi_events
from
tests
.
bidi
.
network
import
(
    
RESPONSE_COMPLETED_EVENT
    
STYLESHEET_RED_COLOR
    
get_cached_url
    
get_next_event_for_url
)
from
webdriver
.
bidi
import
error
pytest
.
mark
.
parametrize
(
    
"
use_collector
"
    
[
True
False
]
)
pytest
.
mark
.
asyncio
async
def
test_cached_stylesheet
(
    
bidi_session
    
url
    
inline
    
setup_network_test
    
top_context
    
add_data_collector
    
use_collector
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
            
RESPONSE_COMPLETED_EVENT
        
]
    
)
    
events
=
network_events
[
RESPONSE_COMPLETED_EVENT
]
    
cached_link_css_url
=
url
(
get_cached_url
(
"
text
/
css
"
STYLESHEET_RED_COLOR
)
)
    
page_with_cached_css
=
inline
(
        
f
"
"
"
        
<
head
>
<
link
rel
=
"
stylesheet
"
type
=
"
text
/
css
"
href
=
"
{
cached_link_css_url
}
"
>
<
/
head
>
        
<
body
>
test
page
with
cached
link
stylesheet
<
/
body
>
        
"
"
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
top_context
[
"
context
"
]
        
url
=
page_with_cached_css
        
wait
=
"
complete
"
    
)
    
await
wait_for_bidi_events
(
bidi_session
events
2
timeout
=
2
)
    
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
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
top_context
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
    
await
wait_for_bidi_events
(
bidi_session
events
4
timeout
=
2
)
    
cached_events
=
events
[
2
:
]
    
cached_css_event
=
get_next_event_for_url
(
cached_events
cached_link_css_url
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
        
if
use_collector
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
cached_css_event
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
                
data_type
=
"
response
"
                
collector
=
collector
            
)
        
else
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
cached_css_event
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
data_type
=
"
response
"
            
)
