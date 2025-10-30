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
    
BEFORE_REQUEST_SENT_EVENT
    
STYLESHEET_RED_COLOR
    
get_cached_url
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
asyncio
async
def
test_unique_request_ids
(
    
bidi_session
    
url
    
inline
    
setup_network_test
    
top_context
    
fetch
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
        
]
    
)
    
events
=
network_events
[
BEFORE_REQUEST_SENT_EVENT
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
    
await
fetch
(
"
data
:
text
/
plain
1
"
)
    
await
fetch
(
"
data
:
text
/
plain
2
"
)
    
await
fetch
(
"
data
:
text
/
plain
3
"
)
    
await
fetch
(
"
data
:
text
/
plain
4
"
)
    
await
wait_for_bidi_events
(
bidi_session
events
8
timeout
=
2
)
    
ids
=
list
(
map
(
lambda
event
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
events
)
)
    
assert
len
(
ids
)
=
=
len
(
set
(
ids
)
)
