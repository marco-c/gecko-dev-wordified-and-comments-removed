import
asyncio
import
pytest
pytestmark
=
pytest
.
mark
.
asyncio
from
.
.
import
AUTH_REQUIRED_EVENT
PAGE_EMPTY_HTML
async
def
test_unsubscribe
(
bidi_session
new_tab
url
)
:
    
await
bidi_session
.
session
.
subscribe
(
events
=
[
AUTH_REQUIRED_EVENT
]
)
    
await
bidi_session
.
session
.
unsubscribe
(
events
=
[
AUTH_REQUIRED_EVENT
]
)
    
events
=
[
]
    
async
def
on_event
(
method
data
)
:
        
events
.
append
(
data
)
    
remove_listener
=
bidi_session
.
add_event_listener
(
AUTH_REQUIRED_EVENT
on_event
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
new_tab
[
"
context
"
]
        
url
=
url
(
            
"
/
webdriver
/
tests
/
support
/
http_handlers
/
authentication
.
py
?
realm
=
testrealm
"
        
)
        
wait
=
"
none
"
    
)
    
await
asyncio
.
sleep
(
0
.
5
)
    
assert
len
(
events
)
=
=
0
    
remove_listener
(
)
