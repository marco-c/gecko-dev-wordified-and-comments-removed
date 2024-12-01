import
pytest
from
tests
.
support
.
sync
import
AsyncPoll
from
webdriver
.
error
import
TimeoutException
pytest
.
mark
.
asyncio
async
def
test_unsubscribe_from_module
(
bidi_session
new_tab
inline
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
"
browsingContext
"
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
"
browsingContext
"
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
    
remove_listener_domContentLoaded
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
domContentLoaded
"
on_event
    
)
    
remove_listener_load
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
load
"
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
inline
(
"
"
)
    
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
0
)
    
remove_listener_domContentLoaded
(
)
    
remove_listener_load
(
)
pytest
.
mark
.
asyncio
async
def
test_subscribe_to_module_unsubscribe_from_one_event
(
      
bidi_session
wait_for_event
wait_for_future_safe
new_tab
inline
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
"
browsingContext
"
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
"
browsingContext
.
domContentLoaded
"
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
_
)
:
        
events
.
append
(
method
)
    
remove_listener_domContentLoaded
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
domContentLoaded
"
on_event
    
)
    
remove_listener_load
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
load
"
on_event
    
)
    
on_entry_added
=
wait_for_event
(
"
browsingContext
.
load
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
new_tab
[
"
context
"
]
url
=
inline
(
"
"
)
    
)
    
await
wait_for_future_safe
(
on_entry_added
)
    
assert
len
(
events
)
=
=
1
    
assert
"
browsingContext
.
domContentLoaded
"
not
in
events
    
remove_listener_domContentLoaded
(
)
    
remove_listener_load
(
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
"
browsingContext
.
load
"
]
)
