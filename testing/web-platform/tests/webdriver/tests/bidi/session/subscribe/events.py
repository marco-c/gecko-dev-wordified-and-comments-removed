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
new_tab
      
wait_for_event
wait_for_future_safe
inline
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
    
on_context_load
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
on_context_load
)
    
assert
len
(
events
)
=
=
2
    
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
wait_for_future_safe
      
inline
new_tab
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
data
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
    
on_entry_added
=
wait_for_event
(
"
browsingContext
.
domContentLoaded
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
2
    
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
wait_for_future_safe
      
new_tab
inline
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
2
    
await
subscribe_events
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
2
    
remove_listener_domContentLoaded
(
)
    
remove_listener_load
(
)
