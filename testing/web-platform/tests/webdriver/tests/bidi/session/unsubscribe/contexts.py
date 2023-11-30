import
pytest
from
.
.
.
import
create_console_api_message
recursive_compare
pytest
.
mark
.
asyncio
async
def
test_unsubscribe_from_one_context
(
    
bidi_session
top_context
new_tab
wait_for_event
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
new_tab
[
"
context
"
]
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
"
log
.
entryAdded
"
on_event
)
    
await
create_console_api_message
(
bidi_session
top_context
"
text1
"
)
    
assert
len
(
events
)
=
=
0
    
on_entry_added
=
wait_for_event
(
"
log
.
entryAdded
"
)
    
expected_text
=
await
create_console_api_message
(
bidi_session
new_tab
"
text2
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
    
recursive_compare
(
        
{
            
"
text
"
:
expected_text
        
}
        
events
[
0
]
    
)
    
remove_listener
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
log
.
entryAdded
"
]
contexts
=
[
new_tab
[
"
context
"
]
]
    
)
pytest
.
mark
.
asyncio
async
def
test_unsubscribe_from_top_context_with_iframes
(
    
bidi_session
    
top_context
    
test_page_same_origin_frame
)
:
    
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
test_page_same_origin_frame
wait
=
"
complete
"
    
)
    
contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
root
=
top_context
[
"
context
"
]
)
    
assert
len
(
contexts
[
0
]
[
"
children
"
]
)
=
=
1
    
frame
=
contexts
[
0
]
[
"
children
"
]
[
0
]
    
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
"
log
.
entryAdded
"
on_event
)
    
await
create_console_api_message
(
bidi_session
frame
"
text1
"
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
pytest
.
mark
.
asyncio
async
def
test_unsubscribe_from_child_context
(
    
bidi_session
    
top_context
    
test_page_same_origin_frame
)
:
    
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
test_page_same_origin_frame
wait
=
"
complete
"
    
)
    
contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
root
=
top_context
[
"
context
"
]
)
    
assert
len
(
contexts
[
0
]
[
"
children
"
]
)
=
=
1
    
frame
=
contexts
[
0
]
[
"
children
"
]
[
0
]
    
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
log
.
entryAdded
"
]
contexts
=
[
frame
[
"
context
"
]
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
"
log
.
entryAdded
"
on_event
)
    
await
create_console_api_message
(
bidi_session
frame
"
text1
"
)
    
await
create_console_api_message
(
bidi_session
top_context
"
text2
"
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
pytest
.
mark
.
asyncio
async
def
test_unsubscribe_from_one_context_after_navigation
(
    
bidi_session
top_context
test_alt_origin
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
test_alt_origin
wait
=
"
complete
"
    
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
log
.
entryAdded
"
]
contexts
=
[
top_context
[
"
context
"
]
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
"
log
.
entryAdded
"
on_event
)
    
await
create_console_api_message
(
bidi_session
top_context
"
text1
"
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
