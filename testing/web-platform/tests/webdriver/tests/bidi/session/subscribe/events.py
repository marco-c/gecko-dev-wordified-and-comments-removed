import
pytest
pytest
.
mark
.
asyncio
async
def
test_subscribe_to_module
(
bidi_session
subscribe_events
wait_for_event
)
:
    
await
subscribe_events
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
_
)
:
        
events
.
append
(
method
)
    
remove_listener_contextCreated
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
contextCreated
"
on_event
    
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
create
(
type_hint
=
"
tab
"
)
    
await
on_entry_added
    
assert
len
(
events
)
=
=
3
    
remove_listener_contextCreated
(
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
test_subscribe_to_one_event_and_then_to_module
(
    
bidi_session
subscribe_events
wait_for_event
)
:
    
await
subscribe_events
(
events
=
[
"
browsingContext
.
contextCreated
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
method
)
    
remove_listener_contextCreated
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
contextCreated
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
contextCreated
"
)
    
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
on_entry_added
    
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
contextCreated
"
in
events
    
await
subscribe_events
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
create
(
type_hint
=
"
tab
"
)
    
await
on_entry_added
    
assert
len
(
events
)
=
=
3
    
remove_listener_contextCreated
(
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
test_subscribe_to_module_and_then_to_one_event_again
(
    
bidi_session
subscribe_events
wait_for_event
)
:
    
await
subscribe_events
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
method
)
    
remove_listener_contextCreated
=
bidi_session
.
add_event_listener
(
        
"
browsingContext
.
contextCreated
"
on_event
    
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
create
(
type_hint
=
"
tab
"
)
    
await
on_entry_added
    
assert
len
(
events
)
=
=
3
    
await
subscribe_events
(
events
=
[
"
browsingContext
.
contextCreated
"
]
)
    
events
=
[
]
    
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
create
(
type_hint
=
"
tab
"
)
    
await
on_entry_added
    
assert
len
(
events
)
=
=
3
    
remove_listener_contextCreated
(
)
    
remove_listener_domContentLoaded
(
)
    
remove_listener_load
(
)
