import
pytest
from
webdriver
.
bidi
.
modules
.
script
import
ContextTarget
from
.
.
.
import
create_console_api_message
recursive_compare
pytestmark
=
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
wait_for_future_safe
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
async
def
test_subscribe_to_one_context_twice
(
    
bidi_session
subscribe_events
top_context
wait_for_event
wait_for_future_safe
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
async
def
test_subscribe_to_one_context_and_then_to_all
(
    
bidi_session
subscribe_events
top_context
new_tab
wait_for_event
wait_for_future_safe
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
text3
"
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
text4
"
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
async
def
test_subscribe_to_all_context_and_then_to_one_again
(
    
bidi_session
subscribe_events
top_context
new_tab
wait_for_event
wait_for_future_safe
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
    
remove_listener
(
)
async
def
test_subscribe_to_top_context_with_iframes
(
    
bidi_session
    
subscribe_events
    
wait_for_event
wait_for_future_safe
    
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
    
remove_listener
(
)
async
def
test_subscribe_to_child_context
(
    
bidi_session
    
subscribe_events
    
wait_for_event
wait_for_future_safe
    
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
    
remove_listener
(
)
pytest
.
mark
.
parametrize
(
"
domain
"
[
"
"
"
alt
"
]
ids
=
[
"
same_origin
"
"
cross_origin
"
]
)
async
def
test_subscribe_to_child_context_and_navigate_sibling_frame
(
    
bidi_session
    
subscribe_events
    
wait_for_event
wait_for_future_safe
    
top_context
    
test_page_multiple_frames
    
inline
    
domain
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
browsingContext
.
load
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
browsingContext
.
load
"
on_event
)
    
url
=
inline
(
"
<
div
>
foo
<
/
div
>
"
domain
=
domain
)
    
on_load
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
script
.
evaluate
(
        
expression
=
f
"
document
.
querySelectorAll
(
'
iframe
'
)
[
1
]
.
src
=
'
{
url
}
'
"
        
target
=
ContextTarget
(
top_context
[
"
context
"
]
)
        
await_promise
=
False
    
)
    
await
wait_for_future_safe
(
on_load
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
events
[
0
]
[
"
context
"
]
=
=
frame_2
[
"
context
"
]
    
assert
events
[
0
]
[
"
url
"
]
=
=
url
    
remove_listener
(
)
async
def
test_subscribe_to_child_context_and_navigate_top_context
(
    
bidi_session
    
subscribe_events
    
wait_for_event
wait_for_future_safe
    
top_context
    
test_page_multiple_frames
    
test_page
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
    
await
subscribe_events
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
browsingContext
.
load
"
on_event
)
    
on_load
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
top_context
[
"
context
"
]
url
=
test_page
wait
=
"
complete
"
    
)
    
await
wait_for_future_safe
(
on_load
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
events
[
0
]
[
"
context
"
]
=
=
top_context
[
"
context
"
]
    
assert
events
[
0
]
[
"
url
"
]
=
=
test_page
    
remove_listener
(
)
async
def
test_subscribe_to_child_context_and_navigate_nested_frame
(
    
bidi_session
    
subscribe_events
    
wait_for_event
wait_for_future_safe
    
top_context
    
test_page_nested_frames
    
inline
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
test_page_nested_frames
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
    
frame_level_1
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
    
assert
len
(
frame_level_1
[
"
children
"
]
)
=
=
1
    
frame_level_2
=
frame_level_1
[
"
children
"
]
[
0
]
    
await
subscribe_events
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
contexts
=
[
frame_level_1
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
browsingContext
.
load
"
on_event
)
    
url
=
inline
(
"
<
div
>
foo
<
/
div
>
"
)
    
on_load
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
script
.
evaluate
(
        
expression
=
f
"
document
.
querySelector
(
'
iframe
'
)
.
contentDocument
.
querySelector
(
'
iframe
'
)
.
src
=
'
{
url
}
'
"
        
target
=
ContextTarget
(
top_context
[
"
context
"
]
)
        
await_promise
=
False
    
)
    
await
wait_for_future_safe
(
on_load
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
events
[
0
]
[
"
context
"
]
=
=
frame_level_2
[
"
context
"
]
    
assert
events
[
0
]
[
"
url
"
]
=
=
url
    
remove_listener
(
)
