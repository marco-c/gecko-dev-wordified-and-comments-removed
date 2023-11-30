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
test_subscribe_to_one_context
(
    
bidi_session
subscribe_events
top_context
new_tab
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
new_tab
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
top_context
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
pytest
.
mark
.
asyncio
async
def
test_subscribe_to_one_context_twice
(
    
bidi_session
subscribe_events
top_context
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
subscribe_events
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
top_context
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
    
assert
len
(
events
)
=
=
1
    
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
test_subscribe_to_one_context_and_then_to_all
(
    
bidi_session
subscribe_events
top_context
new_tab
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
    
buffered_event_expected_text
=
await
create_console_api_message
(
        
bidi_session
new_tab
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
top_context
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
    
events
=
[
]
    
await
subscribe_events
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
)
    
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
buffered_event_expected_text
        
}
        
events
[
0
]
    
)
    
expected_text
=
await
create_console_api_message
(
bidi_session
new_tab
"
text3
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
2
    
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
1
]
    
)
    
expected_text
=
await
create_console_api_message
(
bidi_session
top_context
"
text4
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
2
]
    
)
    
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
test_subscribe_to_all_context_and_then_to_one_again
(
    
bidi_session
subscribe_events
top_context
new_tab
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
log
.
entryAdded
"
]
)
    
await
subscribe_events
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
    
await
create_console_api_message
(
bidi_session
top_context
"
text1
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
test_subscribe_to_top_context_with_iframes
(
    
bidi_session
    
subscribe_events
    
wait_for_event
    
top_context
    
test_page_multiple_frames
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
test_page_multiple_frames
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
2
    
frame_1
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
    
frame_2
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
1
]
    
await
subscribe_events
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
    
await
create_console_api_message
(
bidi_session
frame_1
"
text1
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
    
await
create_console_api_message
(
bidi_session
frame_2
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
2
    
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
test_subscribe_to_child_context
(
    
bidi_session
    
subscribe_events
    
wait_for_event
    
top_context
    
test_page_multiple_frames
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
test_page_multiple_frames
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
2
    
frame_1
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
    
frame_2
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
1
]
    
await
subscribe_events
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
frame_1
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
    
await
create_console_api_message
(
bidi_session
top_context
"
text1
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
    
await
create_console_api_message
(
bidi_session
frame_2
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
2
    
remove_listener
(
)
